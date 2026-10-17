import base64
import asyncio
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import DB_CHANNEL, DELETED_TEXT
from database import db


def encode(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode()).decode().strip("=")


def decode(payload: str) -> str:
    return base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)).decode()


def make_payload(first_id: int, last_id: int = None) -> str:
    k = abs(DB_CHANNEL)
    if last_id is None or last_id == first_id:
        return encode(f"get-{first_id * k}")
    return encode(f"get-{first_id * k}-{last_id * k}")


def decode_ids(payload: str):
    parts = decode(payload).split("-")
    k = abs(DB_CHANNEL)
    if parts[0] != "get":
        raise ValueError("bad payload")
    if len(parts) == 2:
        return [int(parts[1]) // k]
    a, b = int(parts[1]) // k, int(parts[2]) // k
    return list(range(min(a, b), max(a, b) + 1))


def link_for(client, payload: str) -> str:
    return f"https://t.me/{client.me.username}?start={payload}"


def readable_time(seconds: int) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    out = []
    if h:
        out.append(f"{h} HOUR")
    if m:
        out.append(f"{m} MINUTES")
    if s and not h:
        out.append(f"{s} SECONDS")
    return " ".join(out) or "0 SECONDS"


async def get_unjoined_buttons(client, user_id: int):
    rows = []
    for ch in await db.get_fsubs():
        cid = ch["_id"]
        joined = False
        try:
            member = await client.get_chat_member(cid, user_id)
            if member.status not in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
                joined = True
        except UserNotParticipant:
            if ch.get("request") and await db.has_request(cid, user_id):
                joined = True
        except Exception as e:
            print(f"[fsub] cannot check {cid}: {e}")
            joined = True
        if not joined:
            rows.append([InlineKeyboardButton(f"📢 JOIN {ch['title']}", url=ch["link"])])
    return rows


async def fetch_messages(client, ids):
    msgs = []
    for i in range(0, len(ids), 200):
        chunk = ids[i : i + 200]
        while True:
            try:
                res = await client.get_messages(DB_CHANNEL, chunk)
                break
            except FloodWait as e:
                await asyncio.sleep(e.value)
        msgs.extend(res if isinstance(res, list) else [res])
    return [m for m in msgs if m and not m.empty]


async def auto_delete(client, chat_id, sent_msgs, warn_msg, payload, delay):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, [m.id for m in sent_msgs])
    except Exception:
        pass
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=link_for(client, payload))]]
    )
    try:
        await warn_msg.edit_text(
            DELETED_TEXT,
            reply_markup=btn,
            disable_web_page_preview=True,
        )
    except Exception:
        pass

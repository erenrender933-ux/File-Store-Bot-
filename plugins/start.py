import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import (
    ADMINS, START_PIC, START_TEXT, ABOUT_TEXT, HELP_TEXT, MORE_CHANNELS_URL,
    FORCE_SUB_TEXT, AUTO_DELETE_TEXT, PROTECT_CONTENT,
)
from database import db
from helpers import (
    decode_ids, fetch_messages, get_unjoined_buttons, link_for,
    readable_time, auto_delete,
)


def home_buttons():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("• ᴍᴏʀᴇ ᴄʜᴀɴɴᴇʟs •", url=MORE_CHANNELS_URL)],
            [
                InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("ʜᴇʟᴘ •", callback_data="help"),
            ],
        ]
    )


def back_buttons():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="home"),
          InlineKeyboardButton("ᴄʟᴏsᴇ•", callback_data="close")]]
    )


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await db.add_user(message.from_user.id)

    if len(message.command) > 1:
        return await send_files(client, message, message.command[1])

    text = START_TEXT.format(mention=message.from_user.mention)
    if START_PIC:
        await message.reply_photo(START_PIC, caption=text, reply_markup=home_buttons())
    else:
        await message.reply_text(text, reply_markup=home_buttons())


@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    await message.reply_text(HELP_TEXT, reply_markup=back_buttons())


async def send_files(client, message, payload):
    user_id = message.from_user.id

    # 1) check sᴜʙsᴄʀɪᴘᴛɪᴏɴᴡ
    status = await message.reply_text("<b>🔍 ᴄʜᴇᴄᴋɪɴɢ sᴜʙsᴄʀɪᴘᴛɪᴏɴ...</b>")
    rows = await get_unjoined_buttons(client, user_id)
    if rows:
        rows.append([InlineKeyboardButton("♻️ ʀᴇʟᴏᴀᴅ", url=link_for(client, payload))])
        return await status.edit_text(
            FORCE_SUB_TEXT.format(mention=message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(rows),
            disable_web_page_preview=True,
        )
    # 2) please wait
    await status.edit_text("<b>Please Wait..</b>")
    try:
        ids = decode_ids(payload)
    except Exception:
        return await status.edit_text("<b>❌ INVALID LINK.</b>")

    msgs = await fetch_messages(client, ids)
    if not msgs:
        return await status.edit_text("<b>❌ FILE NOT FOUND.</b>")
    await status.delete()

    # 3) send files instantly
    sent = []
    for m in msgs:
        while True:
            try:
                c = await m.copy(user_id, protect_content=PROTECT_CONTENT)
                sent.append(c)
                break
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"[send] {e}")
                break

    # 4) warning + auto delete
    delay = await db.get_delete_time()
    warn = await message.reply_text(AUTO_DELETE_TEXT.format(time=readable_time(delay)))
    asyncio.create_task(auto_delete(client, user_id, sent, warn, payload, delay))


@Client.on_callback_query()
async def callbacks(client, query):
    data = query.data
    if data == "close":
        await query.message.delete()
    else:
        if data == "home":
            text, kb = START_TEXT.format(mention=query.from_user.mention), home_buttons()
        elif data == "about":
            text, kb = ABOUT_TEXT, back_buttons()
        else:
            text, kb = HELP_TEXT, back_buttons()
        if query.message.photo:
            await query.message.edit_caption(text, reply_markup=kb)
        else:
            await query.message.edit_text(text, reply_markup=kb)
    await query.answer()


@Client.on_chat_join_request()
async def join_request(client, req):
    if not await db.is_fsub(req.chat.id):
        return
    is_new = await db.add_request(req.chat.id, req.from_user.id)
    if not is_new:
        return
    goal = await db.bump_goal(req.chat.id)
    if goal:  # goal completed -> notify admins
        for admin_id in ADMINS:
            try:
                await client.send_message(
                    admin_id,
                    f"🎯 <b>GOAL COMPLETED!</b>\n\n"
                    f"Channel: <code>{req.chat.id}</code> ({req.chat.title})\n"
                    f"Requests: {goal['count']}/{goal['goal']}",
                )
            except Exception:
                pass

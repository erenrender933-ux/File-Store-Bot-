import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import ADMINS, DB_CHANNEL, MAX_FSUB
from database import db
from helpers import make_payload, link_for, readable_time

admin = filters.private & filters.user(ADMINS)


# ---------- AUTO LINK: admin sends any file -> stored in DB channel -> link ----------
@Client.on_message(admin & filters.media)
async def auto_link(client, message):
    try:
        stored = await message.copy(DB_CHANNEL)
    except Exception as e:
        return await message.reply_text(f"❌ Cannot store file in DB channel:\n{e}")
    link = link_for(client, make_payload(stored.id))
    await message.reply_text(
        f"<b>✅ File stored!\n\nHere is your link:</b>\n\n{link}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔁 Share URL", url=f"https://t.me/share/url?url={link}")]]
        ),
    )


@Client.on_message(admin & filters.command("genlink"))
async def genlink(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a file with /genlink")
    stored = await message.reply_to_message.copy(DB_CHANNEL)
    await message.reply_text(
        f"<b>Here is your link:</b>\n\n{link_for(client, make_payload(stored.id))}",
        disable_web_page_preview=True,
    )


@Client.on_message(admin & filters.command("batch"))
async def batch(client, message):
    # /batch first_post_link last_post_link  (post links from DB channel)
    if len(message.command) != 3:
        return await message.reply_text("Usage: /batch first_post_link last_post_link")
    try:
        first = int(message.command[1].rstrip("/").split("/")[-1])
        last = int(message.command[2].rstrip("/").split("/")[-1])
    except ValueError:
        return await message.reply_text("Invalid links.")
    await message.reply_text(
        f"<b>Here is your batch link:</b>\n\n{link_for(client, make_payload(first, last))}",
        disable_web_page_preview=True,
    )


# ---------- force sub management (max 6) ----------
@Client.on_message(admin & filters.command("addfsub"))
async def addfsub(client, message):
    # /addfsub -100xxxx            -> normal join
    # /addfsub -100xxxx request    -> join request mode
    args = message.command[1:]
    if not args:
        return await message.reply_text("Usage: /addfsub channel_id [request]")
    try:
        cid = int(args[0])
    except ValueError:
        return await message.reply_text("Channel id must be like -100xxxxxxxxxx")
    request = len(args) > 1 and args[1].lower() == "request"

    existing = [c["_id"] for c in await db.get_fsubs()]
    if cid not in existing and len(existing) >= MAX_FSUB:
        return await message.reply_text(f"❌ Maximum {MAX_FSUB} force-sub channels allowed.")
    try:
        chat = await client.get_chat(cid)
        invite = await client.create_chat_invite_link(cid, creates_join_request=request)
    except Exception as e:
        return await message.reply_text(f"❌ Error: {e}\nMake bot admin with invite-link permission.")
    await db.add_fsub(cid, chat.title, invite.invite_link, request)
    total = len(await db.get_fsubs())
    await message.reply_text(
        f"✅ Added <b>{chat.title}</b> ({'request' if request else 'normal'})\nTotal: {total}/{MAX_FSUB}"
    )


@Client.on_message(admin & filters.command("delfsub"))
async def delfsub(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /delfsub channel_id  or  /delfsub all")
    if message.command[1].lower() == "all":
        await db.clear_fsub()
        return await message.reply_text("✅ All force-sub channels removed.")
    try:
        await db.del_fsub(int(message.command[1]))
    except ValueError:
        return await message.reply_text("Invalid channel id.")
    await message.reply_text("✅ Removed.")


@Client.on_message(admin & filters.command("fsubs"))
async def fsubs(client, message):
    chans = await db.get_fsubs()
    if not chans:
        return await message.reply_text("No force-sub channels set.")
    text = f"<b>Force-sub channels ({len(chans)}/{MAX_FSUB}):</b>\n\n"
    for i, c in enumerate(chans, 1):
        text += f"{i}. {c['title']} — <code>{c['_id']}</code> ({'request' if c.get('request') else 'normal'})\n"
    await message.reply_text(text)


# ---------- request goals ----------
@Client.on_message(admin & filters.command("setgoal"))
async def setgoal(client, message):
    # /setgoal -100xxxx 1000
    if len(message.command) != 3 or not message.command[2].isdigit():
        return await message.reply_text("Usage: /setgoal channel_id goal_number\nExample: /setgoal -100123456 1000")
    try:
        cid = int(message.command[1])
    except ValueError:
        return await message.reply_text("Invalid channel id.")
    chans = {c["_id"]: c for c in await db.get_fsubs()}
    if cid not in chans or not chans[cid].get("request"):
        return await message.reply_text("❌ Channel must be added with: /addfsub channel_id request")
    goal = int(message.command[2])
    await db.set_goal(cid, goal)
    await message.reply_text(f"🎯 Goal set: {goal} join requests for <b>{chans[cid]['title']}</b>.\nYou will be notified when completed.")


@Client.on_message(admin & filters.command("goals"))
async def goals(client, message):
    gs = await db.get_goals()
    if not gs:
        return await message.reply_text("No goals set. Use /setgoal channel_id number")
    chans = {c["_id"]: c for c in await db.get_fsubs()}
    text = "<b>🎯 GOAL PROGRESS</b>\n\n"
    for g in gs:
        title = chans.get(g["_id"], {}).get("title", g["_id"])
        pct = min(100, int(g["count"] * 100 / g["goal"]))
        state = "✅ Completed" if g["done"] else "⏳ Running"
        text += f"• {title}\n  {g['count']}/{g['goal']} ({pct}%) — {state}\n\n"
    await message.reply_text(text)


@Client.on_message(admin & filters.command("delgoal"))
async def delgoal(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /delgoal channel_id")
    try:
        await db.del_goal(int(message.command[1]))
    except ValueError:
        return await message.reply_text("Invalid channel id.")
    await message.reply_text("✅ Goal removed.")


# ---------- settings / stats ----------
@Client.on_message(admin & filters.command("setdelete"))
async def setdelete(client, message):
    if len(message.command) < 2 or not message.command[1].isdigit():
        cur = await db.get_delete_time()
        return await message.reply_text(f"Usage: /setdelete seconds\nCurrent: {readable_time(cur)}")
    secs = int(message.command[1])
    await db.set_delete_time(secs)
    await message.reply_text(f"✅ Auto delete time set to {readable_time(secs)}")


@Client.on_message(admin & filters.command("users"))
async def users(client, message):
    await message.reply_text(f"<b>Total users:</b> {await db.total_users()}")


@Client.on_message(admin & filters.command("broadcast"))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message with /broadcast")
    ok = fail = 0
    status = await message.reply_text("Broadcasting...")
    for uid in await db.all_users():
        try:
            await message.reply_to_message.copy(uid)
            ok += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            fail += 1
            await db.del_user(uid)
    await status.edit_text(f"✅ Done\nSuccess: {ok}\nFailed: {fail}")

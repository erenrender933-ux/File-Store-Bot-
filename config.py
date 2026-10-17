import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "FileStoreBot")

DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "0"))
ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split() if x.lstrip("-").isdigit()]

AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "600"))
START_PIC = os.environ.get("START_PIC", "")
MORE_CHANNELS_URL = os.environ.get("MORE_CHANNELS_URL", "https://t.me/telegram")
PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False").lower() == "true"

MAX_FSUB = 6

START_TEXT = (
    "<b>ʙᴀᴋᴀ ~ » {mention}\n\n"
    "<blockquote>ɪ ᴀᴍ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ, ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ "
    "ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.</blockquote></b>"
)

ABOUT_TEXT = (
    "<b>ᴀʙᴏᴜᴛ ᴍᴇ\n\n"
    "<blockquote>◈ ʙᴏᴛ : ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ\n"
    "◈ ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ 3\n"
    "◈ ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ\n"
    "◈ ᴅᴀᴛᴀʙᴀsᴇ : <a href=\"https://www.mongodb.com\">ᴍᴏɴɢᴏ ᴅʙ</a>\n"
    "◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=\"https://t.me/Eren_157\">ᴇʀᴇɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ</a></blockquote>"
)

HELP_TEXT = (
    "<b>/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n"
    "/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n"
    "sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n"
    "ᴊᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!\n\n"
    "ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ @Eren_157</b>"
)

FORCE_SUB_TEXT = (
    "<b>ʙᴀᴋᴀ ~ » {mention}\n\n"
    "<blockquote>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</blockquote></b>"
    "<b><blockquote>‣ ᴄʟɪᴄᴋ -  <a href=\"https://t.me/How_Download_Links_3\">ᴛᴜᴛᴏʀɪᴀʟ</a></blockquote></b>"
)

AUTO_DELETE_TEXT = (
    "<b><blockquote>‣ ɴᴏᴛᴇ: ᴛʜɪs ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ɪɴ {time}. ꜰᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ɴᴏᴡ..!\n</blockquote>"
    "<blockquote>‣ ʜᴏᴡ ᴛᴏ ꜰᴏʀᴡᴀʀᴅ - <a href=\"https://t.me/How_Download_Links_3/10\">ᴛᴜᴛᴏʀɪᴀʟ</a></blockquote></b>"
)

DELETED_TEXT = (
    "<b><blockqoute>ʏᴏᴜʀ ᴠɪᴅᴇᴏ / ғɪʟᴇ ɪs sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ !!</blockquote>\n\n"
    "<blockquote>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴅᴇʟᴇᴛᴇᴅ ᴠɪᴅᴇᴏ / ғɪʟᴇ 👇</blockquote></b>"
)

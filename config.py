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
    "<b>BAKA ~ » {mention}\n\n"
    "I AM FILE STORE BOT, I CAN STORE PRIVATE FILES IN SPECIFIED CHANNEL "
    "AND OTHER USERS CAN ACCESS IT FROM SPECIAL LINK.</b>"
)

ABOUT_TEXT = (
    "<b>ABOUT ME\n\n"
    "• BOT : FILE STORE BOT\n"
    "• LANGUAGE : PYTHON 3\n"
    "• LIBRARY : PYROGRAM\n"
    "• DATABASE : MONGODB\n"
    "• DEVELOPER : YOUR NAME</b>"
)

HELP_TEXT = (
    "<b>/start : START THE BOT\n"
    "/help : HELP RELATED BOT\n\n"
    "SIMPLY CLICK ON LINK AND START THE BOT\n"
    "JOIN ALL CHANNELS AND TRY AGAIN THATS IT.....!\n\n"
    "DEVELOPED BY YOUR NAME</b>"
)

FORCE_SUB_TEXT = (
    "<b>⚠️ YOU MUST JOIN OUR CHANNELS TO GET YOUR FILE.\n\n"
    "JOIN ALL CHANNELS BELOW, THEN CLICK TRY AGAIN 👇</b>"
)

AUTO_DELETE_TEXT = (
    "<b>⚠️ THIS FILE WILL BE DELETED IN {time}.\n"
    "FORWARD IT SOMEWHERE ELSE BEFORE DOWNLOADING.</b>"
)

DELETED_TEXT = (
    "<b>YOUR VIDEO / FILE IS SUCCESSFULLY DELETED !!\n\n"
    "CLICK BELOW BUTTON TO GET YOUR DELETED VIDEO / FILE 👇</b>"
)

from os import getenv
#
API_ID = int(getenv("API_ID", "28872999"))
API_HASH = getenv("API_HASH", "7bab29feade5c8d36a5b47645eb769cb")

BOT_TOKEN = getenv("BOT_TOKEN", "6410981698:AAGLfD-VHkZUHWq8VwIGKQzJcPRkX_wtgJg")
  
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://phil:phil9665@cluster0.vvs2pmw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

SUDO_USERS = getenv("SUDO_USERS",  "1086394021")
OWNER_ID = int(getenv("OWNER_ID", "1965472544"))

LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1002461084481)
ANIME_CHAR_CHANNEL_ID = -1002139511906

# DO NOT CHANGE BELOW CODES.

SUDO_USERS = list(map(int, SUDO_USERS.split()))

if not OWNER_ID in SUDO_USERS:
  SUDO_USERS.append(OWNER_ID)

MAIN_GROUP_ID = -1002461084481
SUPPORT_GROUP = "International_animez_community" # ENTER WITHOUT "@"
SUPPORT_CHANNEL = "YxH_Homeland" # ENTER WITHOUT "@"

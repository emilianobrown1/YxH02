from os import getenv
#
API_ID = int(getenv("API_ID", "8460373"))
API_HASH = getenv("API_HASH", "83d8e423197251216303abfcbed9e820")

BOT_TOKEN = getenv("BOT_TOKEN", "")
  
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://splgame:25102005@cluster0.ykb8p.mongodb.net/?retryWrites=true&w=majority")

SUDO_USERS = getenv("SUDO_USERS", "5903688119 1965472544 5910101206")
OWNER_ID = int(getenv("OWNER_ID", "5903688119"))

LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1001876710416)
CHAR_CHANNEL_ID = 0

# DO NOT CHANGE BELOW CODES.

SUDO_USERS = list(map(int, SUDO_USERS.split()))
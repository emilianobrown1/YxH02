from os import getenv
#
API_ID = int(getenv("API_ID", "8460373"))
API_HASH = getenv("API_HASH", "83d8e423197251216303abfcbed9e820")

BOT_TOKEN = getenv("BOT_TOKEN", "7006726437:AAEUqcQLuKiUbiF_gM26TrEl47abHPoyGjQ")
  
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://phil:phil@cluster0.vvs2pmw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

SUDO_USERS = getenv("SUDO_USERS",  "1965472544")
OWNER_ID = int(getenv("OWNER_ID", "5903688119"))

LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1001876710416)
ANIME_CHAR_CHANNEL_ID = -1002139511906

# DO NOT CHANGE BELOW CODES.

SUDO_USERS = list(map(int, SUDO_USERS.split()))

MAIN_GROUP_ID = -1002014537230
SUPPORT_GROUP = "Devil_ani" # ENTER WITHOUT "@"
SUPPORT_CHANNEL = "Devil_ani" # ENTER WITHOUT "@"

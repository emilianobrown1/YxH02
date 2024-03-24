from os import getenv
#
API_ID = int(getenv("API_ID", "8460373"))
API_HASH = getenv("API_HASH", "83d8e423197251216303abfcbed9e820")

BOT_TOKEN = dic[TOKEN_NUMBER]
  
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://splgame:25102005@cluster0.ykb8p.mongodb.net/?retryWrites=true&w=majority")

SUDO_USER = getenv("SUDO_USERS", "5903688119 1965472544 5910101206")
OWNER_ID = int(getenv("OWNER_ID", "5903688119"))

LOG_GROUP_ID = getenv("LOG_GROUP_ID", -1001876710416)

SUDO_USERS = []

for x in SUDO_USER.split():
  SUDO_USERS.append(int(x))

TESTERS = []
TESTERS += SUDO_USERS

TEST_GROUPS = [-1001816477508, -1001876710416]

CHAR_CHANNEL_ID = -1001989936059
EVENTS_GROUP_ID = -1002055004688

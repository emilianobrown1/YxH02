from pyrogram import Client, idle
from config import *

YxH = Client(
        ":YxH:",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="YxH/Plugins")
    )

from pyrogram import Client, idle
from config import *
import os

YxH = Client(
    ":YxH:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="YxH/Plugins")
)

def __init__():
    os.makedirs("Characters", exist_ok=True)
    YxH.start()
    print("Bot Started.")
    idle()

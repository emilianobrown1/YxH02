from pyrogram import Client, idle
import os
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "YxHBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="YxH/Plugins")
)

if __name__ == "__main__":
    os.makedirs("Characters", exist_ok=True)
    app.start()
    print("✅ Bot Started.")
    idle()

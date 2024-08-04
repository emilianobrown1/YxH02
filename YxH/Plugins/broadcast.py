from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
from ..Database.chats import get_all_chats
from ..Database.users import get_all_users
from config import OWNER_ID

DEV_USERS = [OWNER_ID]
if 1965472544 not in DEV_USERS:
    DEV_USERS.append(1965472544)

@Client.on_message(filters.command(["broadcast", "pbroadcast"]) & filters.user(DEV_USERS))
async def broadcast(client, message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
    
    sent = 0
    pinned = 0
    chats = await get_all_chats()
    CASTED = []
    
    for chat in chats:
        chat_id = chat.chat_id  # Assuming chat_id is an attribute of the chat object
        if chat_id in CASTED:
            continue
        try:
            if message.reply_to_message:
                forwarded_msg = await client.forward_messages(chat_id, y, x)
                sent += 1
                CASTED.append(chat_id)
                if message.command[0][1].lower() == "p":
                    await client.pin_chat_message(chat_id, forwarded_msg.id)
                    pinned += 1
            else:
                sent_msg = await client.send_message(chat_id, query)
                sent += 1
                CASTED.append(chat_id)
                if message.command[0][1].lower() == "p":
                    await client.pin_chat_message(chat_id, sent_msg.id)
                    pinned += 1
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            continue
    
    try:
        await message.reply_text(
            f"**Broadcasted Message In {sent} Chats and pinned in {pinned} Chats**"
        )
    except Exception:
        pass
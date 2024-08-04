from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
from ..Database.users import get_all_users
from config import OWNER_ID

DEV_USERS = [OWNER_ID]
if 1965472544 not in DEV_USERS:
    DEV_USERS.append(1965472544)

@Client.on_message(filters.command("ubroadcast") & filters.user(DEV_USERS))
async def ubr(client, message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/ubroadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
    
    sent = 0
    users = await get_all_users()
    CASTED = []
    
    for user in users:
        user_id = user.user_id  # Assuming user_id is an attribute of the user object
        if user_id in CASTED:
            continue
        try:
            if message.reply_to_message:
                await client.forward_messages(user_id, y, x)
                sent += 1
                CASTED.append(user_id)
            else:
                await client.send_message(user_id, query)
                sent += 1
                CASTED.append(user_id)
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            continue
    
    try:
        await message.reply_text(
            f"**Broadcasted Message to {sent} Users !**"
        )
    except Exception:
        pass
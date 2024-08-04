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
        query = None
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
        x, y = None, None
    
    sent = 0
    pinned = 0
    try:
        chats = await get_all_chats()
        print(f"Retrieved {len(chats)} chats")
    except Exception as e:
        print(f"Error retrieving chats: {e}")
        return

    for chat in chats:
        chat_id = chat.chat_id
        try:
            if message.reply_to_message:
                forwarded_msg = await client.forward_messages(chat_id, y, x)
                sent += 1
                if message.command[0][1].lower() == "p":
                    await client.pin_chat_message(chat_id, forwarded_msg.id)
                    pinned += 1
            else:
                sent_msg = await client.send_message(chat_id, query)
                sent += 1
                if message.command[0][1].lower() == "p":
                    await client.pin_chat_message(chat_id, sent_msg.id)
                    pinned += 1
        except FloodWait as e:
            flood_time = int(e.x)
            print(f"FloodWait of {flood_time} seconds for chat {chat_id}")
            await asyncio.sleep(flood_time)
        except Exception as e:
            print(f"Error in broadcasting to chat {chat_id}: {e}")

    try:
        await message.reply_text(
            f"**Broadcasted Message In {sent} Chats and pinned in {pinned} Chats**"
        )
    except Exception as e:
        print(f"Error in replying to message: {e}")

@Client.on_message(filters.command("ubroadcast") & filters.user(DEV_USERS))
async def ubr(client, message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
        query = None
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/ubroadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
        x, y = None, None
    
    sent = 0
    try:
        users = await get_all_users()
        print(f"Retrieved {len(users)} users")
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return

    for user in users:
        user_id = user.user_id
        try:
            if message.reply_to_message:
                await client.forward_messages(user_id, y, x)
                sent += 1
            else:
                await client.send_message(user_id, query)
                sent += 1
        except FloodWait as e:
            flood_time = int(e.x)
            print(f"FloodWait of {flood_time} seconds for user {user_id}")
            await asyncio.sleep(flood_time)
        except Exception as e:
            print(f"Error in broadcasting to user {user_id}: {e}")

    try:
        await message.reply_text(
            f"**Broadcasted Message to {sent} Users !**"
        )
    except Exception as e:
        print(f"Error in replying to message: {e}")
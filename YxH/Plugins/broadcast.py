from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
from ..Database.chats import get_all_chats
from ..Database.users import get_all_users
from config import SUDO_USERS

@Client.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast_message(client, message):
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message
        use_copy = True
    else:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("Please provide a broadcast message or reply to a message to broadcast.")
        broadcast_text = parts[1]
        use_copy = False

    # Get all chats and users (each entry contains both ID and pickled info)
    chat_entries = await get_all_chats()  # List of {"chat_id": ..., "info": ...}
    user_entries = await get_all_users()  # List of {"user_id": ..., "info": ...}

    total_success = 0  
    total_failed = 0  

    # Broadcast to chats
    for entry in chat_entries:
        chat_id = entry["chat_id"]  # Access chat_id from the database document
        try:
            if use_copy:
                await client.copy_message(chat_id, message.chat.id, broadcast_msg.message_id)
            else:
                await client.send_message(chat_id, broadcast_text)
            total_success += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            total_failed += 1
            print(f"Failed to send to chat {chat_id}: {e}")

    for entry in chats:
        chat_id = entry["id"]  # Get from the database document's chat_id
        try:
            if use_copy:
                await client.copy_message(chat_id, message.chat.id, broadcast_msg.message_id)
            else:
                await client.send_message(chat_id, broadcast_text)
            total_success += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            total_failed += 1
            print(f"Failed to send to chat {chat_id}: {e}")

    # Broadcast to users
    for entry in users:
        user_id = entry["id"]  # Get from the database document's user_id
        try:
            if use_copy:
                await client.copy_message(user_id, message.chat.id, broadcast_msg.message_id)
            else:
                await client.send_message(user_id, broadcast_text)
            total_success += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            total_failed += 1
            print(f"Failed to send to user {user_id}: {e}")

    await message.reply_text(f"Broadcast completed! Success: {total_success}, Failures: {total_failed}")
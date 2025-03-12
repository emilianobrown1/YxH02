from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
from Database.chats import get_all_chats
from Database.users import get_all_users
from config import SUDO_USERS

@Client.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast_message(client, message):
    """
    This command broadcasts a message to all chats and DMs.
    You can either reply to a message (including media) to broadcast it,
    or pass a text message as an argument.
    """
    # Determine what to broadcast
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message
        use_copy = True  # use copy_message for media and complex messages
    else:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.reply_text("Please provide a broadcast message or reply to a message to broadcast.")
        broadcast_text = parts[1]
        use_copy = False

    # Fetch all chats and users from the database
    chats = await get_all_chats()  # should return list of chat objects with chat_id attribute
    users = await get_all_users()  # should return list of user objects with user_id attribute

    total_success = 0
    total_failed = 0

    # Broadcast to group/supergroup chats
    for chat in chats:
        try:
            if use_copy:
                await client.copy_message(chat.chat_id, message.chat.id, broadcast_msg.message_id)
            else:
                await client.send_message(chat.chat_id, broadcast_text)
            total_success += 1
            # To help avoid hitting rate limits, add a small delay
            await asyncio.sleep(0.1)
        except FloodWait as e:
            # If a FloodWait is raised, wait for the required time
            await asyncio.sleep(e.x)
        except Exception as e:
            total_failed += 1
            print(f"Failed to send to chat {chat.chat_id}: {e}")

    # Broadcast to user DMs
    for user in users:
        try:
            if use_copy:
                await client.copy_message(user.user_id, message.chat.id, broadcast_msg.message_id)
            else:
                await client.send_message(user.user_id, broadcast_text)
            total_success += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            total_failed += 1
            print(f"Failed to send to user {user.user_id}: {e}")

    await message.reply_text(f"Broadcast completed! Success: {total_success}, Failures: {total_failed}")
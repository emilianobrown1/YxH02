from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
import asyncio
from ..Database.chats import get_all_chats
from ..Database.users import get_all_users
from config import OWNER_ID

DEV_USERS = set([OWNER_ID, 1965472544])  # Using a set for efficient lookup

async def send_message_with_flood_control(client, recipient_id, message, pin=False):
    try:
        if message.reply_to_message:
            sent_msg = await message.reply_to_message.forward(recipient_id)
        else:
            sent_msg = await client.send_message(recipient_id, message.text.split(None, 1)[1])
        
        if pin:
            await client.pin_chat_message(recipient_id, sent_msg.id)
        return True, None
    except FloodWait as e:
        return False, e.value
    except RPCError as e:
        print(f"Error sending message to {recipient_id}: {e}")
        return False, 0

async def broadcast_to_targets(client, message, targets, is_user_broadcast=False):
    sent, pinned = 0, 0
    total = len(targets)

    for i, target in enumerate(targets, 1):
        target_id = target.user_id if is_user_broadcast else target.chat_id
        success, wait_time = await send_message_with_flood_control(
            client, target_id, message, 
            pin=(not is_user_broadcast and message.command[0][1].lower() == 'p')
        )

        if success:
            sent += 1
            if not is_user_broadcast and message.command[0][1].lower() == 'p':
                pinned += 1
        
        if wait_time:
            await asyncio.sleep(wait_time)

        if i % 20 == 0:  # Progress update every 20 items
            progress_msg = f"Progress: {i}/{total} {'users' if is_user_broadcast else 'chats'}"
            await message.reply_text(progress_msg, quote=True)

    return sent, pinned

@Client.on_message(filters.command(["broadcast", "pbroadcast"]) & filters.user(DEV_USERS))
async def broadcast(client, message):
    if not (message.reply_to_message or len(message.command) > 1):
        return await message.reply_text(
            "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
        )

    try:
        chats = await get_all_chats()
        sent, pinned = await broadcast_to_targets(client, message, chats)
        await message.reply_text(
            f"**Broadcasted Message In {sent} Chats and pinned in {pinned} Chats**"
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("ubroadcast") & filters.user(DEV_USERS))
async def ubr(client, message):
    if not (message.reply_to_message or len(message.command) > 1):
        return await message.reply_text(
            "**Usage**:\n/ubroadcast [MESSAGE] or [Reply to a Message]"
        )

    try:
        users = await get_all_users()
        sent, _ = await broadcast_to_targets(client, message, users, is_user_broadcast=True)
        await message.reply_text(f"**Broadcasted Message to {sent} Users!**")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
from pyrogram import Client, filters
from ..Database.users import get_user
from config import SUDO_USERS, OWNER_ID

@Client.on_message(filters.command("block") & filters.user(SUDO_USERS + [OWNER_ID]))
async def block_user_command(client, message):
    user_id = None
    
    # Check if the command is a reply to a user's message
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        # Otherwise, try to get the user ID from the command arguments
        if len(message.command) > 1:
            user_id = int(message.command[1])
    
    # If no user_id is found, reply with usage instructions
    if not user_id:
        await message.reply("Please reply to a user or provide a user ID to block.")
        return

    # Fetch user data
    user_data = await get_user(user_id)
    if not user_data:
        await message.reply("User not found. They need to start the bot first.")
        return
    
    user = pickle.loads(user_data['info'])

    # Block user check
    if user.blocked:
        await message.reply("User is already blocked.")
        return
    
    # Perform block operation
    user.block_user()
    await user.update()

    await message.reply(f"User {user_id} has been blocked.")


@Client.on_message(filters.command("unblock") & filters.user(SUDO_USERS + [OWNER_ID]))
async def unblock_user_command(client, message):
    user_id = None
    
    # Check if the command is a reply to a user's message
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        # Otherwise, try to get the user ID from the command arguments
        if len(message.command) > 1:
            user_id = int(message.command[1])
    
    # If no user_id is found, reply with usage instructions
    if not user_id:
        await message.reply("Please reply to a user or provide a user ID to unblock.")
        return

    # Fetch user data
    user_data = await get_user(user_id)
    if not user_data:
        await message.reply("User not found.")
        return
    
    user = pickle.loads(user_data['info'])

    # Unblock user check
    if not user.blocked:
        await message.reply("User is not blocked.")
        return
    
    # Perform unblock operation
    user.unblock_user()
    await user.update()

    await message.reply(f"User {user_id} has been unblocked.")
from pyrogram import Client, filters
from ..Database.users import get_user
from ..Class.user import User
from config import SUDO_USERS, OWNER_ID
import pickle

@Client.on_message(filters.command("block") & filters.user(SUDO_USERS + [OWNER_ID]))
async def block_user_command(client, message):
    user_id = await get_user_id(message)
    if not user_id:
        await message.reply("Please reply to a user or provide a valid user ID to block.")
        return

    user = await get_user_object(user_id)
    if not user:
        await message.reply("User not found. They need to start the bot first.")
        return

    if user.blocked:
        await message.reply("User is already blocked.")
        return

    user.block_user()
    await user.update()

    await message.reply(f"User {user_id} has been blocked.")

@Client.on_message(filters.command("unblock") & filters.user(SUDO_USERS + [OWNER_ID]))
async def unblock_user_command(client, message):
    user_id = await get_user_id(message)
    if not user_id:
        await message.reply("Please reply to a user or provide a valid user ID to unblock.")
        return

    user = await get_user_object(user_id)
    if not user:
        await message.reply("User not found.")
        return

    if not user.blocked:
        await message.reply("User is not blocked.")
        return

    user.unblock_user()
    await user.update()

    await message.reply(f"User {user_id} has been unblocked.")

async def get_user_id(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            return int(message.command[1])
        except ValueError:
            return None
    return None

async def get_user_object(user_id):
    user_data = await get_user(user_id)
    if not user_data:
        return None
    return pickle.loads(user_data['info'])
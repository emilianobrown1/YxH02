from pyrogram import Client, filters
from ..Database.users import get_user
from config import SUDO_USERS
from ..Utils.strings import block_text
from ..universal_decorator import YxH

@Client.on_message(filters.command("block") & filters.user(SUDO_USERS))
@YxH()
async def block_user_command(client, message, user):
    if len(message.command) < 2:
        await message.reply("Please specify a user ID.")
        return

    user_id = int(message.command[1])
    user = await get_user(user_id)

    if user:
        user.blocked = True
        await user.update()
        await message.reply(f"User {user_id} has been blocked.")
    else:
        await message.reply("User not found.")

@Client.on_message(filters.command("unblock") & filters.user(SUDO_USERS))
@YxH()
async def unblock_user_command(client, message, user):
    if len(message.command) < 2:
        await message.reply("Please specify a user ID.")
        return

    user_id = int(message.command[1])
    user = await get_user(user_id)

    if user:
        user.blocked = False
        await user.update()
        await message.reply(f"User {user_id} has been unblocked.")
    else:
        await message.reply("User not found.")

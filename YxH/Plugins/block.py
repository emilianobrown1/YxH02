from pyrogram import Client, filters
from ..Database.users import get_user
from ..Class.user import User
from config import SUDO_USERS, OWNER_ID

@Client.on_message(filters.command("block") & filters.user(SUDO_USERS + [OWNER_ID]))
async def block_user_command(client, message):
    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        if len(message.command) > 1:
            user_id = int(message.command[1])

    if not user_id:
        await message.reply("Please reply to a user or provide a user ID to block.")
        return

    user_data = await get_user(user_id)
    if not user_data:
        await message.reply("User not found. They need to start the bot first.")
        return

    user = pickle.loads(user_data['info'])

    print(f"Before blocking, user {user_id} blocked status: {user.blocked}")

    if user.blocked:
        await message.reply("User is already blocked.")
        return

    user.block_user()
    await user.update()

    print(f"After blocking, user {user_id} blocked status: {user.blocked}")

    await message.reply(f"User {user_id} has been blocked.")


@Client.on_message(filters.command("unblock") & filters.user(SUDO_USERS + [OWNER_ID]))
async def unblock_user_command(client, message):
    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        if len(message.command) > 1:
            user_id = int(message.command[1])

    if not user_id:
        await message.reply("Please reply to a user or provide a user ID to unblock.")
        return

    user_data = await get_user(user_id)
    if not user_data:
        await message.reply("User not found.")
        return

    user = pickle.loads(user_data['info'])

    print(f"Before unblocking, user {user_id} blocked status: {user.blocked}")

    if not user.blocked:
        await message.reply("User is not blocked.")
        return

    user.unblock_user()
    await user.update()

    print(f"After unblocking, user {user_id} blocked status: {user.blocked}")

    await message.reply(f"User {user_id} has been unblocked.")
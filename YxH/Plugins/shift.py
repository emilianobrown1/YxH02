from pyrogram import Client, filters
from . import YxH
from ..Class.user import User

@Client.on_message(filters.command("shift"))
async def shift_command_handler(client, message, user):
    if len(message.command) != 3:
        await message.reply("Usage: /shift <old_user_id> <new_user_id>")
        return

    old_user_id = int(message.command[1])
    new_user_id = int(message.command[2])

    user = User(old_user_id)

    # Perform the shift and merge
    response = await user.shift_user_data(old_user_id, new_user_id)

    await message.reply(response)

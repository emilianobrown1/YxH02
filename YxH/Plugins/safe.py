from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user

@app.on_message(filters.command("safegd"))
async def safe_gold(client, message, user):
    user = await get_user_from_message(message)  # Function to get User object from message
    if user is None:
        return
    amount = int(message.text.split()[1])
    result = await user.transfer_to_treasure(0, 0, amount)
    await message.reply(result)

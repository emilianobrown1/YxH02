from pyrogram import Client, filters
from YxH.Database import db
import pickle

@Client.on_message(filters.command("safexgd"))
async def safegd(client, message, user):
    user = await get_user_from_message(message)
    if user is None:
        return
    try:
        amount = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("Please provide a valid amount of gold to transfer.")
        return
    result = await transfer_to_treasure(user, amount)
    await message.reply(result)

async def get_user_from_message(message):
    user_id = message.from_user.id
    user_data = await db.users.find_one({'user_id': user_id})
    if user_data:
        user = pickle.loads(user_data['info'])
        return user
    else:
        await message.reply("User not found in database.")
        return None

async def transfer_to_treasure(user, gold):
    if not user.treasure_state:
        return "Transfer failed: Treasure is locked."
    if user.gold < gold:
        return "Transfer failed: Insufficient gold."
    user.gold -= gold
    if not user.treasure:
        user.treasure = [0, 0, 0]
    user.treasure[0] += gold
    await user.update()
    return f"Transfer successful! Transferred {gold} 📯 to treasure"
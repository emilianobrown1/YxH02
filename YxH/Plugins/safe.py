from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user

@Client.on_message(filters.command("safegd"))
async def safegd(_, m, u):
    user = await get_user_from_message(message)  # Function to get User object from message
    if user is None:
        return
    try:
        amount = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("Please provide a valid amount of gold to transfer.")
        return

    result = await user.transfer_to_treasure(0, 0, amount)
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

async def transfer_to_treasure(self, crystals, gems, gold):
        if not self.treasure_state:
            return "Transfer failed: Treasure is locked."

        if self.gold < gold:
            return "Transfer failed: Insufficient gold."

        self.gold -= gold
        self.treasure[0] += gold

        # Update user in the database
        await self.update()

        return f"Transfer successful! Transferred {gold} 📯 to treasure"

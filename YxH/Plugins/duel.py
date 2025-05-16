from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..Class.duel import Duel
import YxH.duel_callback as duel_callback
from ..Database.users import get_user

# In-memory duel storage for demo; replace with DB or Redis for persistence
active_duels = {}

@Client.on_message(filters.command("duel") & filters.reply)
async def start_duel(client, message):
    from_user = message.from_user.id
    to_user = message.reply_to_message.from_user.id

    if from_user == to_user:
        await message.reply("You cannot duel yourself!")
        return

    # Check if either user is already in duel
    if from_user in active_duels or to_user in active_duels:
        await message.reply("Either you or the opponent is already in a duel!")
        return

    # Load users from DB - optional: check user existence or restrictions
    user1 = await get_user(from_user)
    user2 = await get_user(to_user)
    if not user1 or not user2:
        await message.reply("One of the users is not registered in the game.")
        return

    duel = Duel(from_user, to_user)
    active_duels[from_user] = duel
    active_duels[to_user] = duel

    text = f"Duel started between {duel.players[from_user]['name']} (you) and {duel.players[to_user]['name']} (opponent)!\n\n"
    text += f"Turn: {duel.players[duel.turn]['name']}"

    keyboard = duel_callback.get_duel_keyboard(from_user)

    await message.reply(text, reply_markup=keyboard)
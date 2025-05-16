from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from ..Class.duel import Duel
from ..Database.users import get_user, update_user
import random

active_duels = {}

@Client.on_message(filters.command("duel") & filters.reply)
async def start_duel(client, message):
    from_user = message.from_user.id
    to_user = message.reply_to_message.from_user.id

    if from_user == to_user:
        await message.reply("You cannot duel yourself!")
        return

    if from_user in active_duels or to_user in active_duels:
        await message.reply("Either you or the opponent is already in a duel!")
        return

    user1 = await get_user(from_user)
    user2 = await get_user(to_user)
    if not user1 or not user2:
        await message.reply("One of the users is not registered in the game.")
        return

    # Check gold cost
    cost = 100_000
    if user1.get("gold", 0) < cost or user2.get("gold", 0) < cost:
        await message.reply("Both players must have at least 100,000 gold to start a duel.")
        return

    # Deduct gold cost
    user1["gold"] -= cost
    user2["gold"] -= cost
    await update_user(from_user, user1)
    await update_user(to_user, user2)

    duel = Duel(from_user, to_user)
    active_duels[from_user] = duel
    active_duels[to_user] = duel

    text = (
        f"Duel started between {duel.players[from_user]['name']} (you) "
        f"and {duel.players[to_user]['name']} (opponent)!\n\n"
        f"Turn: {duel.players[duel.turn]['name']}"
    )
    keyboard = get_duel_keyboard(from_user)
    await message.reply(text, reply_markup=keyboard)

def get_duel_keyboard(user_id):
    from .duel_callback import get_duel_keyboard
    return get_duel_keyboard(user_id)
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from ..Class.duel import Duel
from ..Class.user import User
import random

active_duels = {}

@Client.on_message(filters.command("duel") & filters.reply)
async def start_duel(client, message):
    from_user = message.from_user
    to_user = message.reply_to_message.from_user

    if from_user.id == to_user.id:
        await message.reply("You cannot duel yourself!")
        return

    if from_user.id in active_duels or to_user.id in active_duels:
        await message.reply("Either you or the opponent is already in a duel!")
        return

    # Initialize User objects (assuming `User` class takes a user object)
    u1 = User(from_user)
    u2 = User(to_user)

    cost = 100_000
    if u1.gold < cost:
        await message.reply("You don’t have enough gold to duel! (Need 100,000 gold)")
        return
    if u2.gold < cost:
        await message.reply("Your opponent doesn’t have enough gold to duel! (Need 100,000 gold)")
        return

    # Deduct gold (since `User` class doesn't have `add_gold`, manually subtract and update)
    u1.gold -= cost
    u2.gold -= cost
    await u1.update()  # Save changes to the database
    await u2.update()

    duel = Duel(from_user.id, to_user.id)
    active_duels[from_user.id] = duel
    active_duels[to_user.id] = duel

    text = (
        f"Duel started between {duel.players[from_user.id]['name']} (you) "
        f"and {duel.players[to_user.id]['name']} (opponent)!\n\n"
        f"Turn: {duel.players[duel.turn]['name']}"
    )
    keyboard = get_duel_keyboard(from_user.id)
    await message.reply(text, reply_markup=keyboard)

def get_duel_keyboard(user_id):
    from .duel_callback import get_duel_keyboard
    return get_duel_keyboard(user_id)
from pyrogram import Client, filters
from ..Database.users import get_user
from ..Class.user import User
from ..Class.duel import Duel
from ..Class.duel_state import active_duels
from ..Utils.duel_utils import get_duel_keyboard
import random

@Client.on_message(filters.command("duel") & filters.reply)
async def start_duel(client, message):
    from_user = message.from_user
    to_user = message.reply_to_message.from_user

    if from_user.id == to_user.id:
        await message.reply("You cannot duel yourself!")
        return

    if from_user.id in active_duels or to_user.id in active_duels:
        await message.reply("Either you or your opponent is already in a duel!")
        return

    # Get User instances
    u1 = await get_user(from_user.id)
    u2 = await get_user(to_user.id)

    cost = 100_000
    if u1.gold < cost:
        await message.reply("You don’t have enough gold to duel! (Need 100,000 gold)")
        return
    if u2.gold < cost:
        await message.reply("Your opponent doesn’t have enough gold to duel! (Need 100,000 gold)")
        return

    try:
        # Deduct gold first
        u1.gold -= cost
        u2.gold -= cost
        await u1.update()
        await u2.update()

        # Initialize duel WITH PROPER ARGUMENTS (user1_id, user2_id)
        duel = Duel(u1.user.id, u2.user.id)  # Removed bet_amount parameter
        await duel.initialize()

        # Store duel state
        active_duels[u1.user.id] = duel
        active_duels[u2.user.id] = duel

        # Get character names from duel instance
        text = (
            f"⚔️ Duel started between {duel.players[u1.user.id]['name']} (you) "
            f"and {duel.players[u2.user.id]['name']} (opponent)!\n\n"
            f"🎮 Turn: {duel.players[duel.turn]['name']}"
        )
        keyboard = get_duel_keyboard(u1.user.id)
        await message.reply(text, reply_markup=keyboard)

    except Exception as e:
        # Rollback gold deduction if duel creation fails
        u1.gold += cost
        u2.gold += cost
        await u1.update()
        await u2.update()
        await message.reply(f"❌ Failed to start duel: {str(e)}")
        # Cleanup active duels if any
        active_duels.pop(u1.user.id, None)
        active_duels.pop(u2.user.id, None)
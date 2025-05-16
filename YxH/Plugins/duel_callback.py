from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from ..Class.duel import Duel
from ..Database.users import get_user, update_user
from .duel import active_duels
import random
import pickle

def get_duel_keyboard(user_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Attack", callback_data=f"duel_attack:{user_id}"),
            InlineKeyboardButton("Special", callback_data=f"duel_special:{user_id}")
        ],
        [
            InlineKeyboardButton("Heal", callback_data=f"duel_heal:{user_id}"),
            InlineKeyboardButton("Exit Duel", callback_data=f"duel_exit:{user_id}")
        ]
    ])

@Client.on_callback_query(filters.regex(r"^duel_(attack|special|heal|exit):(\d+)$"))
async def duel_callback(client: Client, callback: CallbackQuery):
    action_part, user_id_str = callback.data.split(":")
    user_id = int(user_id_str)
    from_user = callback.from_user.id

    if user_id != from_user:
        await callback.answer("It's not your turn!", show_alert=True)
        return

    duel = active_duels.get(user_id)
    if not duel:
        await callback.answer("You are not in an active duel.", show_alert=True)
        return

    if duel.turn != user_id and action_part != "exit":
        await callback.answer("Wait for your turn!", show_alert=True)
        return

    if action_part == "exit":
        for uid in list(duel.players.keys()):
            active_duels.pop(uid, None)
        await callback.message.edit("Duel ended prematurely.")
        await callback.answer()
        return

    if action_part == "attack":
        damage = duel.attack(user_id)
        result_text = f"You attacked and dealt {damage} damage."
    elif action_part == "special":
        damage = duel.special(user_id)
        result_text = f"You used special and dealt {damage} damage."
    elif action_part == "heal":
        heal_amount = duel.heal(user_id)
        result_text = f"You healed yourself for {heal_amount} HP."
    else:
        await callback.answer("Invalid action.", show_alert=True)
        return

    if duel.is_finished():
        players = list(duel.players.keys())
        hp1 = duel.health[players[0]]
        hp2 = duel.health[players[1]]
        winner_id = players[0] if hp1 > hp2 else players[1]
        loser_id = players[1] if hp1 > hp2 else players[0]

        winner_user = await get_user(winner_id)
        loser_user = await get_user(loser_id)

        transfer_msg = ""
        if winner_user and loser_user:
            loser_collection = loser_user.get("collection", {})
            if loser_collection:
                char_to_transfer = random.choice(list(loser_collection.keys()))
                
                # Update winner's collection
                winner_user.setdefault("collection", {})
                winner_user["collection"][char_to_transfer] = winner_user["collection"].get(char_to_transfer, 0) + 1
                
                # Update loser's collection
                loser_user["collection"][char_to_transfer] -= 1
                if loser_user["collection"][char_to_transfer] <= 0:
                    del loser_user["collection"][char_to_transfer]
                
                # Save changes
                await update_user(winner_id, pickle.dumps(winner_user))
                await update_user(loser_id, pickle.dumps(loser_user))
                
                transfer_msg = f"\n\nYou won! You received character **{char_to_transfer}** from your opponent."
            else:
                transfer_msg = "\n\nYou won! But your opponent has no characters to transfer."

        for uid in list(duel.players.keys()):
            active_duels.pop(uid, None)

        await callback.message.edit(
            f"{result_text}\n\nDuel finished!\nWinner: <a href='tg://user?id={winner_id}'>Player</a>{transfer_msg}",
            disable_web_page_preview=True,
            parse_mode="html"
        )
        await callback.answer()
        return

    status_text = (
        f"{result_text}\n\n"
        f"{duel.get_status(duel.turn)}\n"
        f"{duel.get_health_bar(duel.turn)}\n\n"
        f"Last moves:\n{duel.get_log()}"
    )
    keyboard = get_duel_keyboard(duel.turn)
    await callback.message.edit(status_text, reply_markup=keyboard)
    await callback.answer()
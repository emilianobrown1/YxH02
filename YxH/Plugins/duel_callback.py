from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from ..Class.duel import Duel
from YxH.Plugins import duel
import asyncio

active_duels = duel.active_duels  # share duel dict

def get_duel_keyboard(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Attack", callback_data=f"duel_attack:{user_id}"),
         InlineKeyboardButton("Special", callback_data=f"duel_special:{user_id}")],
        [InlineKeyboardButton("Heal", callback_data=f"duel_heal:{user_id}")]
    ])

@Client.on_callback_query(filters.regex(r"^duel_(attack|special|heal):(\d+)$"))
async def duel_handler(client: Client, callback_query: CallbackQuery):
    action, user_id_str = callback_query.data.split(":")
    user_id = int(user_id_str)

    duel_instance = active_duels.get(user_id)
    if not duel_instance:
        await callback_query.answer("No active duel found.", show_alert=True)
        return

    if duel_instance.turn != callback_query.from_user.id:
        await callback_query.answer("It's not your turn!", show_alert=True)
        return

    if duel_instance.is_finished():
        winner_id = None
        for uid, hp in duel_instance.health.items():
            if hp > 0:
                winner_id = uid
        await callback_query.message.edit(f"Duel over! Winner: {duel_instance.players[winner_id]['name']}")
        # Cleanup duel
        for uid in duel_instance.players:
            active_duels.pop(uid, None)
        return

    result_text = ""
    if action == "duel_attack":
        damage = duel_instance.attack(user_id)
        result_text = f"Attack dealt {damage} damage."
    elif action == "duel_special":
        damage = duel_instance.special(user_id)
        result_text = f"Special attack dealt {damage} damage."
    elif action == "duel_heal":
        heal = duel_instance.heal(user_id)
        result_text = f"Healed {heal} HP."

    status_1 = duel_instance.get_health_bar(list(duel_instance.players.keys())[0])
    status_2 = duel_instance.get_health_bar(list(duel_instance.players.keys())[1])
    log = duel_instance.get_log()

    new_text = (
        f"{log}\n\n"
        f"{status_1}\n"
        f"{status_2}\n\n"
        f"Turn: {duel_instance.players[duel_instance.turn]['name']}\n"
        f"{result_text}"
    )
    keyboard = get_duel_keyboard(duel_instance.turn)
    await callback_query.message.edit(new_text, reply_markup=keyboard)
    await callback_query.answer()
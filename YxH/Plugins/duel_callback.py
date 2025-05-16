from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from ..Class.duel import Duel
from ..Class.duel_state import active_duels
from ..Utils.duel_utils import get_duel_keyboard
from ..Database.users import get_user
import random

@Client.on_callback_query(filters.regex(r"^duel_(attack|special|heal|exit):(\d+)$"))
async def handle_duel_actions(client: Client, callback: CallbackQuery):
    try:
        action_part = callback.matches[0].group(1)
        user_id = int(callback.matches[0].group(2))
        from_user = callback.from_user.id

        if user_id != from_user:
            await callback.answer("🚫 It's not your turn!", show_alert=True)
            return

        duel = active_duels.get(user_id)
        if not duel:
            await callback.answer("❌ Duel session expired!", show_alert=True)
            return

        if action_part == "exit":
            for uid in duel.player_ids:
                active_duels.pop(uid, None)
            await callback.message.edit("⚔️ Duel cancelled!")
            await callback.answer()
            return

        if duel.turn != user_id:
            await callback.answer("⏳ Wait for your turn!", show_alert=True)
            return

        # Process actions
        if action_part == "attack":
            damage = duel.attack(user_id)
            result_text = f"⚔️ Attacked for {damage} damage!"
        elif action_part == "special":
            damage = duel.special(user_id)
            result_text = f"🌀 Special move dealt {damage} damage!"
        elif action_part == "heal":
            heal_amount = duel.heal(user_id)
            result_text = f"❤️ Healed for {heal_amount} HP!"
        else:
            await callback.answer("❌ Invalid action", show_alert=True)
            return

        if duel.is_finished():
            winner_id = max(duel.player_ids, key=lambda x: duel.health[x])
            loser_id = min(duel.player_ids, key=lambda x: duel.health[x])

            winner = await get_user(winner_id)
            loser = await get_user(loser_id)

            transfer_msg = ""
            if loser.collection:
                stolen_char = random.choice(list(loser.collection.keys()))
                loser.collection[stolen_char] -= 1
                if loser.collection[stolen_char] <= 0:
                    del loser.collection[stolen_char]
                winner.collection[stolen_char] = winner.collection.get(stolen_char, 0) + 1
                transfer_msg = f"\n\n🏆 Won {stolen_char} from opponent!"
                await winner.update()
                await loser.update()

            for uid in duel.player_ids:
                active_duels.pop(uid, None)

            await callback.message.edit(
                f"🎉 Duel finished!{transfer_msg}\n"
                f"Winner: {winner.user.first_name}",
                reply_markup=None
            )
            await callback.answer()
            return

        status_text = (
            f"{result_text}\n\n"
            f"{duel.get_status(duel.turn)}\n"
            f"{duel.get_health_bar(duel.turn)}\n"
            f"📜 Last moves:\n{duel.get_log()}"
        )
        await callback.message.edit(
            status_text,
            reply_markup=get_duel_keyboard(duel.turn)
        )
        await callback.answer()

    except Exception as e:
        await callback.answer(f"⚠️ Error: {str(e)}", show_alert=True)
        print(f"Duel callback error: {str(e)}")
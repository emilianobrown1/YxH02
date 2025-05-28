from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from ..Class.duel import Duel, Arena
from ..Class.duel_state import active_duels, active_arenas
from ..Utils.duel_utils import get_duel_keyboard, get_arena_keyboard, format_arena_progress
from ..Database.users import get_user

async def process_duel_action(callback: CallbackQuery, duel: Duel, user_id: int, action_part: str, is_arena=False):
    if action_part == "exit":
        if is_arena:
            for uid in duel.player_ids:
                active_arenas.pop(uid, None)
            await callback.message.edit("🏟 Arena cancelled!")
        else:
            for uid in duel.player_ids:
                active_duels.pop(uid, None)
            await callback.message.edit("⚔️ Duel cancelled!")
        return True

    if duel.turn != user_id:
        await callback.answer("⏳ Wait for your turn!", show_alert=True)
        return False

    if action_part.startswith("ability_"):
        ability_index = int(action_part.split("_")[1])
        damage = duel.use_ability(user_id, ability_index)
        ability_name = duel.players[user_id]['abilities'][ability_index]
        result_text = f"⚡ **{ability_name}** dealt {damage} damage!"
    elif action_part == "heal":
        if duel.heal_cooldown[user_id] > 0:
            await callback.answer(f"Heal is on cooldown for {duel.heal_cooldown[user_id]} more turns!", show_alert=True)
            return False
        heal_amount = duel.heal(user_id)
        result_text = f"💚 Healed for {heal_amount} HP!"

    duel.update_cooldowns()
    return result_text

async def handle_duel_finish(callback: CallbackQuery, duel: Duel):
    winner_id = max(duel.player_ids, key=lambda x: duel.health[x])
    loser_id = min(duel.player_ids, key=lambda x: duel.health[x])
    winner = await get_user(winner_id)
    loser = await get_user(loser_id)
    transfer_msg = await duel.reward_winner(winner_id)

    for uid in duel.player_ids:
        active_duels.pop(uid, None)

    await callback.message.edit(
        f"🎉 Duel finished!{transfer_msg}\n"
        f"Winner: {winner.user.first_name}\n\n"
        f"{duel.get_log()}",
        reply_markup=None
    )

async def handle_arena_round_finish(callback: CallbackQuery, arena: Arena):
    arena.process_round_result()

    if arena.finished:
        winner_id, loser_id, result = arena.get_final_results()
        reward_winner_id, reward_loser_id = await arena.reward_players()

        p1_name = callback.message.chat.get_member(arena.player_ids[0]).user.first_name
        p2_name = callback.message.chat.get_member(arena.player_ids[1]).user.first_name

        final_text = "🏆 Arena Finished! 🏆\n\n"
        final_text += f"Final Score: {p1_name}: {arena.scores[arena.player_ids[0]]} - {p2_name}: {arena.scores[arena.player_ids[1]]}\n\n"

        if result == "won":
            winner_name = callback.message.chat.get_member(winner_id).user.first_name
            final_text += f"🎉 Winner: {winner_name}!\n"
            if reward_winner_id is not None:
                final_text += "🎁 Received bonus rewards!"
        else:
            final_text += "🤝 It's a draw! Both players receive a crystal."
            # Rewards for draw are already given in reward_players

        await callback.message.reply(final_text)
        del active_arenas[arena.player_ids[0]]
        del active_arenas[arena.player_ids[1]]
    else:
        if arena.start_next_round():
            next_round_text = f"⚔️ Round {arena.current_round} Starting!\n"
            char1_name, char2_name = arena.get_round_characters()
            next_round_text += f"{char1_name} vs {char2_name}"
            current_turn_player_id = arena.active_duel.turn
            abilities = arena.active_duel.players[current_turn_player_id]['abilities']
            keyboard = get_arena_keyboard(current_turn_player_id, abilities, arena.active_duel.heal_cooldown[current_turn_player_id])
            await callback.message.reply(next_round_text, reply_markup=keyboard)
        else:
            await callback.message.reply("❌ Failed to start the next round.")

@Client.on_callback_query(filters.regex(r"^arena_(ability_\d+|heal|exit):(\d+)$"))
async def handle_arena_actions(client: Client, callback: CallbackQuery):
    try:
        action_part = callback.matches[0].group(1)
        user_id = int(callback.matches[0].group(2))

        if user_id != callback.from_user.id:
            await callback.answer("🚫 It's not your turn!", show_alert=True)
            return

        arena = active_arenas.get(user_id)
        if not arena:
            await callback.answer("❌ Arena session expired!", show_alert=True)
            return

        result_text = await process_duel_action(callback, arena.active_duel, user_id, action_part, is_arena=True)
        if result_text is True or result_text is False:
            return

        if arena.active_duel.is_finished():
            await handle_arena_round_finish(callback, arena)
        else:
            status_text = (
                f"{format_arena_progress(arena)}\n\n"
                f"{result_text}\n\n"
                f"{arena.active_duel.get_status(arena.active_duel.turn)}\n"
                f"{arena.active_duel.get_health_bar(arena.active_duel.turn)}\n\n"
                f"📜 Last moves:\n{arena.active_duel.get_log()}"
            )
            # Get abilities of the current turn player
            current_turn_player_id = arena.active_duel.turn
            abilities = arena.active_duel.players[current_turn_player_id]['abilities']
            keyboard = get_arena_keyboard(
                current_turn_player_id,
                abilities,
                arena.active_duel.heal_cooldown[current_turn_player_id]
            )
            await callback.message.edit(
                status_text,
                reply_markup=keyboard
            )
        await callback.answer()

    except Exception as e:
        await callback.answer(f"⚠️ Error: {str(e)}", show_alert=True)
        print(f"Arena callback error: {str(e)}")

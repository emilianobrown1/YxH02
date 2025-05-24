# Utils/duel_utils.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_duel_keyboard(user_id, abilities, heal_cooldown=0):
    buttons = [
        [
            InlineKeyboardButton(abilities[0], callback_data=f"duel_ability_0:{user_id}"),
            InlineKeyboardButton(abilities[1], callback_data=f"duel_ability_1:{user_id}")
        ],
        [
            InlineKeyboardButton(abilities[2], callback_data=f"duel_ability_2:{user_id}"),
            InlineKeyboardButton(abilities[3], callback_data=f"duel_ability_3:{user_id}")
        ]
    ]
    
    heal_button = InlineKeyboardButton(
        "Heal (25% HP)" if heal_cooldown == 0 else f"Heal (Cooldown: {heal_cooldown})",
        callback_data=f"duel_heal:{user_id}"
    )
    
    buttons.append([
        heal_button,
        InlineKeyboardButton("Exit Duel", callback_data=f"duel_exit:{user_id}")
    ])
    
    return InlineKeyboardMarkup(buttons)


def get_arena_keyboard(arena, user_id):
    buttons = []
    # Keep existing duel keyboard logic
    # Add arena-specific buttons if needed
    return InlineKeyboardMarkup(buttons)

def format_arena_progress(arena):
    p1_score = arena.scores[arena.player_ids[0]]
    p2_score = arena.scores[arena.player_ids[1]]
    
    text = f"🏟 Arena Progress ({arena.current_round}/2)\n"
    text += f"• Round 1: {arena.players[arena.player_ids[0]][0]['name']} vs {arena.players[arena.player_ids[1]][0]['name']}\n"
    text += f"• Round 2: {arena.players[arena.player_ids[0]][1]['name']} vs {arena.players[arena.player_ids[1]][1]['name']}\n\n"
    text += f"📊 Score: {p1_score} - {p2_score}"
    return text
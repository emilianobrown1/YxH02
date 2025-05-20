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
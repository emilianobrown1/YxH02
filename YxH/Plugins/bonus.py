from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import YxH, get_date, get_week
from ..Class import User

@Client.on_message(filters.command("claim"))
@YxH()
async def claim(_, m, user: User):
    date, week = get_date(), get_week()
    today_status: list[bool] = user.bonus.get(date, [False, False, False])
    items: list[str] = ['🔮 Crystal {}', '💎 Gems {}', '📯 Gold {}']
    for i in range(3):
        items[i] = items[i].format('✅' if today_status[i] else '🔘')
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(items[0], callback_data=f"claim|crystal_{user.user.id}")],
            [InlineKeyboardButton(items[1], callback_data=f"claim|gems_{user.user.id}")],
            [InlineKeyboardButton(items[2], callback_data=f"claim|gold_{user.user.id}")],
            [InlineKeyboardButton('Close', callback_data=f'close_{user.user.id}')]
        ]
    )

    await m.reply('Use Buttons Below to Claim Your Bonus.', reply_markup=buttons)
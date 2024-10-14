import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import YxH, get_date, get_week
from ..Class import User

@Client.on_message(filters.command("claim"))
@YxH(private=False)
async def claim(_, m, user: User):
    date, week = get_date(), get_week()
    week_status: list[bool] = user.wbonus.get(week, [False, False, False])
    items: list[str] = ['🔮 Crystal', '💎 Gems (Weekly)', '📯 Gold', '💎 Gems (Daily)']
    for i in range(3):
        items[i] += ' ✅' if week_status[i] else ' 🔘'
    items[3] += ' ✅' if user.dbonus.get(date, False) else ' 🔘'
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(items[0], callback_data=f"claim|crystal_{user.user.id}")],
            [InlineKeyboardButton(items[1], callback_data=f"claim|gems_{user.user.id}")],
            [InlineKeyboardButton(items[2], callback_data=f"claim|gold_{user.user.id}")],
            [InlineKeyboardButton(items[3], callback_data=f"claim|dgems_{user.user.id}")],
            [InlineKeyboardButton('Close', callback_data=f'close_{user.user.id}')],
        ]
    )

    await m.reply('Use Buttons Below to Claim Your Bonus.', reply_markup=buttons)

async def claim_cbq(_, q, u: User):
    data = q.data.split('_')[0].split('|')[1]
    week = get_week()
    date = get_date()
    ws = u.wbonus.get(week, [False, False, False])
    ds = u.dbonus.get(date, False)
    if data == 'crystal':
        if ws[0]:
            return await q.answer()
        u.crystals += 1
        ws[0] = True
        u.wbonus[week] = ws
        await asyncio.gather(
            u.update(),
            q.answer('Collected 1 Crystal.', show_alert=True)
        )
    elif data == 'gems':
        if ws[1]:
            return await q.answer()
        u.gems += 500000
        ws[1] = True
        u.wbonus[week] = ws
        await asyncio.gather(
            u.update(),
            q.answer('Collected 500000 Gems.', show_alert=True)
        )
    elif data == 'gold':
        if ws[2]:
            return await q.answer()
        u.gold += 50000
        ws[2] = True
        u.wbonus[week] = ws
        await asyncio.gather(
            u.update(),
            q.answer('Collected 50000 Gold.', show_alert=True)
        )
    elif data == 'dgems':
        if ds:
            return await q.answer()
        u.gems += 50000
        u.dbonus[date] = True
        await asyncio.gather(
            u.update(),
            q.answer('Collected 50000 Gems.', show_alert=True)
        )
    week_status: list[bool] = u.wbonus.get(week, [False, False, False])
    items: list[str] = ['🔮 Crystal', '💎 Gems (Weekly)', '📯 Gold', '💎 Gems (Daily)']
    for i in range(3):
        items[i] += ' ✅' if week_status[i] else ' 🔘'
    items[3] += ' ✅' if u.dbonus.get(date, False) else ' 🔘'
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(items[0], callback_data=f"claim|crystal_{u.user.id}")],
            [InlineKeyboardButton(items[1], callback_data=f"claim|gems_{u.user.id}")],
            [InlineKeyboardButton(items[2], callback_data=f"claim|gold_{u.user.id}")],
            [InlineKeyboardButton(items[3], callback_data=f"claim|dgems_{u.user.id}")],
            [InlineKeyboardButton('Close', callback_data=f'close_{u.user.id}')],
        ]
    )
    await q.edit_message_reply_markup(reply_markup=buttons)
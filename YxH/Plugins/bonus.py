from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import YxH, get_date, get_week

@Client.on_message(filters.command("claim"))
@YxH()
async def claim(_, m, user):
    date, week = get_date(), get_week()
    l = [date, week]

    
    buttons = InlineKeyboardMarkup(
        [
            
            [InlineKeyboardButton("Crystal 🔮 ✅", callback_data="claim_crystal")],
            [InlineKeyboardButton("Gems 💎 ✅", callback_data="claim_gems")],
            [InlineKeyboardButton("Gold 📯 ✅", callback_data="claim_gold")]
        ]
    )

    if user.bonus == l:
        return await m.reply("You have already claimed your bonus.", reply_markup=buttons)
    
    
    if user.bonus[1] != week:
        await m.reply(
            "Weekly Bonus has been claimed: 550000 gems, 50000 gold, and 1 crystal",
            reply_markup=buttons
        )
        user.gems += 550000
        user.gold += 50000
        user.crystals += 1
        user.bonus = l
        return await user.update()
    
    
    if user.bonus[0] != date:
        await m.reply(
            "Daily Bonus has been claimed: 50000 gems",
            reply_markup=buttons
        )
        user.gems += 50000
        user.bonus = l
        return await user.update()

    
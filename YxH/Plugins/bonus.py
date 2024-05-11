from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import YxH, get_date, get_week

@Client.on_message(filters.command("claim"))
@YxH()
async def claim(_, m, user):
    date, week = get_date(), get_week()
    l = [date, week]

    # Define the new buttons
    buttons = InlineKeyboardMarkup(
        [
            
            [InlineKeyboardButton("Crystal 🔮 ✅", callback_data="claim_crystal")],
            [InlineKeyboardButton("Gems 💎 ✅", callback_data="claim_gems")],
            [InlineKeyboardButton("Gold 📯 ✅", callback_data="claim_gold")]
        ]
    )

    if user.bonus == l:
        return await m.reply("You have already claimed your bonus.", reply_markup=buttons)
    
    # Add your logic here for claiming crystals, gems, and gold
    # Example for claiming crystals
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
    
    # Example for claiming gems
    if user.bonus[0] != date:
        await m.reply(
            "Daily Bonus has been claimed: 50000 gems",
            reply_markup=buttons
        )
        user.gems += 50000
        user.bonus = l
        return await user.update()

    # You will need to add the logic for when the user clicks on the new buttons
    # This is just a placeholder for where you would handle the button callbacks
    
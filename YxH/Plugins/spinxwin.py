from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta  
import time
from ..Database.users import get_user
from . import get_date, YxH


@Client.on_message(filters.command("spinxwin"))
@YxH(private=False)
async def spinxwin(client, message: Message, extra_argument):
    user_id = message.from_user.id
    user = await get_user(user_id)
    
    
    last_spin_time = datetime.fromtimestamp(user.last_spin_time)

    
    if user.spins_left <= 0 and datetime.now() < last_spin_time + timedelta(hours=3):
        time_left = (last_spin_time + timedelta(hours=3)) - datetime.now()
        await message.reply(f"You can spin again in {time_left.seconds // 3600} hours and {(time_left.seconds // 60) % 60} minutes.")
        return

    
    spin_cost = 500000  
    spin_info_text = f"Spin - {spin_cost} gold (cost) 🎰\n\n" \
                     "SPIN REWARD : 🎰\n\n" \
                     "Crystal = 2\n" \
                     "Gems = 75,000\n" \
                     "Gold = 750,000\n" \
                     "Any random character = 1\n"

    
    spin_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Spin 🎰", callback_data="spin")]
    ])

    
    await message.reply(spin_info_text, reply_markup=spin_button)
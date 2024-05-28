from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime  
from ..Database.users import get_user
from . import get_date, YxH
import random

def get_res(prob_perc) -> bool:
    return randon.randint(1, 101) <= prob_perc

@Client.on_message(filters.command("spinxwin"))
@YxH(private=False)
async def spinxwin(_, m: Message, u):
    now = str(datetime.datetime.now()).split(":")[0].replace(" ", "-")
    cur = u.spins.get(now, 0)
    if cur >= 10:
        return await m.reply("No spins left for this hour.")
    if u.gold < 500000:
        return await m.reply(f"You need `{500000-u.gold}` more gold to spin.")
    cry = 2 if get_res(2) else 0
    char = 
    spin_info_text = f"Spin - 500000 gold (cost) 🎰\n\n" \
                     "SPIN REWARD : 🎰\n\n" \
                     "Crystal = 2\n" \
                     "Gems = 75,000\n" \
                     "Gold = 750,000\n" \
                     "Any random character = 1\n"

    
    spin_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Spin 🎰", callback_data="spin")]
    ])

    
    await message.reply(spin_info_text, reply_markup=spin_button)
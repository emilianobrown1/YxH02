from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime  
from ..Database.users import get_user
from . import get_date, YxH
import random
from ..Database.characters import get_anime_character_ids

def get_res() -> int:
    return random.randint(1, 101)

@Client.on_message(filters.command("spinxwin"))
@YxH(private=False)
async def spinxwin(_, m: Message, u):
    now = str(datetime.now()).split(":")[0].replace(" ", "-")
    cur = u.spins.get(now, 0)
    if cur >= 10:
        return await m.reply("No spins left for this hour.")
    if u.gold < 500000:
        return await m.reply(f"You need `{500000-u.gold}` more gold to spin.")
    spin_info_text = f"Spin - 500000 gold (cost) 🎰\n\n" \
                     "SPIN REWARD : 🎰\n\n" \
                     "Crystal = 2\n" \
                     "Gems = 7,500\n" \
                     "Gold = 6,00,000\n" \
                     "Any random character = 1\n\n" \
                     f"Spins Left: {10-cur}"

    
    spin_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Spin 🎰", callback_data=f"spin_{u.user.id}")]
    ])

    
    await m.reply(spin_info_text, reply_markup=spin_button)
    
async def spin_cbq(_, q, u):
    now = str(datetime.now()).split(":")[0].replace(" ", "-")
    cur = u.spins.get(now, 0)
    if cur >= 10:
        return await q.answer("No spins left for this hour.", show_alert=True)
    if u.gold < 500000:
        return await q.answer(f"You need `{500000-u.gold}` more gold to spin.", show_alert=True)
    u.spins[now] = cur + 1
    x = get_res()
    u.gold -= 500000
    if x <= 5:
        txt = "You got 2 Crystals."
        u.crystals += 2
    elif x > 5 and x <= 10:
        char = random.choice(await get_anime_character_ids())
        txt = f"You got a character of ID {char}."
        u.collection[char] = u.collection.get(char, 0) + 1
    elif x > 10 and x <= 40:
        u.gold += 600000
        txt = f"You got 600000 Gold."
    elif x > 40 and x <= 70:
        u.gems += 7500
        txt = f"You got 75000 Gems."
    else:
        txt = "You got nothing, Better Luck Next Time."
    spin_info_text = f"Spin - 500000 gold (cost) 🎰\n\n" \
                     "SPIN REWARD : 🎰\n\n" \
                     "Crystal = 2\n" \
                     "Gems = 7,500\n" \
                     "Gold = 6,00,000\n" \
                     "Any random character = 1\n\n" \
                     f"Spins Left: {10-u.spins[now]}"
    spin_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Spin 🎰", callback_data=f"spin_{u.user.id}")]
    ])
    await q.answer(txt, show_alert=True)
    await q.edit_message_text(spin_info_text, reply_markup=spin_button)
    await u.update()
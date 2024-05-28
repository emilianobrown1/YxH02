from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime  
from ..Database.users import get_user
from . import get_date, YxH
import random
from Database.characters import get_anime_character_ids

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
                     "Any random character = 1\n\n" \
                     f"Spins Left: {10-u.spins}"

    
    spin_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Spin 🎰", callback_data=f"spin_{u.user.id}")]
    ])

    
    await m.reply(spin_info_text, reply_markup=spin_button)
    
async def spin_cbq(_, q, u):
    now = str(datetime.datetime.now()).split(":")[0].replace(" ", "-")
    cur = u.spins.get(now, 0)
    if cur >= 10:
        return await m.reply("No spins left for this hour.")
    if u.gold < 500000:
        return await m.reply(f"You need `{500000-u.gold}` more gold to spin.")
    u.spins[now] = cur + 1
    cry = 2 if get_res(2) else None
    char = random.choice(await get_anime_character_ids()) if get_res(5) else None
    txt = "You got\n\nGold: 600000\nGems: 75000\n"
    u.gold += 600000
    u.gems += 75000
    if cry:
        txt += "Crystals: 2\n"
        u.crystals += 2
    if char:
        txt += f"Character of ID: {char}"
        if char in u.collection:
            u.collection[char] += 1
        else:
            u.collection[char] = 1
    await q.answer(txt, show_alert=True)
    await q.edit_message_text(q.message.caption[:-1] + str(10-u.spins))
    await u.update()
from pyrogram import Client, filters
from . import YxH
import random


percentage_range: list[int] = list(range(10, 51))

@Client.on_message(filters.command("mine"))
@YxH(private=False)
async def mine(_, m, user):
    min_gold_required = 500
    
    try:
        inp: int = int(m.text.split()[1])
    except:
        return await m.reply('Usage: `/mine <amount>`')
    
    if inp > user.gold:
        return await m.reply(f'You only have `{user.gold}` gold.')
    
    if inp < min_gold_required:
        return await m.reply("You need at least `500` gold to start mining.")
    
    success = random.choice([True, False])
    
    percentage = random.choice(percentage_range)
    gold: int = int((inp * percentage)/100)
    
    if success:
        user.gold += gold
        await m.reply(
            f"You mined ⚒️ `{inp}` gold.\n"
            f"User: `{user.gold - gold}` gold before mining.\n"
            f"You've struck gold! 🎉\n"
            f"Percentage of gold found: `{percentage}%`\n"
            f"Reward: `{gold}` gold.📯\n"
            f"User gold after reward: `{user.gold}`"
        )
    else:
        user.gold -= gold
        await m.reply(
            f"You mined ⚒️ `{inp}` gold.\n"
            f"User: `{user.gold + gold}` gold before mining.\n"
            f"No luck this time, keep mining! 💪\n"
            f"Percentage of gold lost: `{percentage}%`\n"
            f"Lost: `{gold}` gold.😞\n"
            f"User gold after loss: `{user.gold}`"
        )
    
    return await user.update()
    
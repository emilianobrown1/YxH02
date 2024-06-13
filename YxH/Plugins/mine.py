from pyrogram import Client, filters
from . import YxH
import random
from .equipments import equipment_data as equipments_data, check_expiry
from datetime import datetime

percentage_range: list[int] = list(range(10, 51))

@Client.on_message(filters.command("mine"))
@YxH(private=False)
async def mine(_, m, user):
    await check_expiry(user)
    min_gold_required = 500
    now = str(datetime.now()).split(":")[0].replace(" ", "-")
    val = user.mine.get(now, 0)
    if val >= 45:
        min = int(str(datetime.now()).split(":")[1])
        after = 30-min if min < 30 else 90-min
        return await m.reply("Mining limit reached, try again after `{after}` minutes.")
    user.mine[now] = val + 1
    try:
        inp = int(m.text.split()[1])
    except IndexError:
        return await m.reply('Usage: `/mine [amount]`')
    
    if inp > user.gold:
        return await m.reply(f'You only have `{user.gold}` gold.')
    
    if inp < min_gold_required:
        return await m.reply("You need at least `500` gold to start mining.")
    
    success = random.choice([True, False])
    
    percentage = random.choice(percentage_range)
    gold = int((inp * percentage) / 100)
    
    if success:
        more = sum([equipments_data[x]["increase"] for x in equipments_data if x[0].lower() in user.rented_items])
        gold += int(gold * more / 100)
        user.gold += gold
        txt = (
            f"You mined ⚒️ `{inp}` gold.\n\n"
            f"Your balance before mining: `{user.gold - gold}` gold.\n\n"
            f"You've struck gold! 🎉\n"
            f"Percentage of gold found: `{percentage}%`\n\n"
            f"Equipments percentage: {more}%\n\n"
            f"Reward: `{gold}` gold.📯\n"
            f"Your gold after reward: `{user.gold}`"
        )
    else:
        user.gold -= gold
        txt = (
            f"You mined ⚒️ `{inp}` gold.\n\n"
            f"Your balance before mining: `{user.gold + gold}` gold.\n\n"
            f"No luck this time, keep mining! 💪\n"
            f"Percentage of gold lost: `{percentage}%`\n\n"
            f"Lost: `{gold}` gold.😞\n\n"
            f"Your gold after loss: `{user.gold}`"
        )
    
    await m.reply_animation("Images/mine.mp4", caption=txt)
    await user.update()

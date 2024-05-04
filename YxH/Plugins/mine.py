from pyrogram import Client, filters
from . import YxH
import random

lis: list[int] = list(range(10, 51))

@Client.on_message(filters.command("mine"))
@YxH(private=False)
async def mine(_, m, user):
    min_gold_required = 500
    try:
        inp: int = int(m.text.split()[1])
    except:
        return await m.reply('`/mine 1000`')
    if inp > user.gold:
        return await m.reply(f'You only having `{user.gold}` gold.')
    if inp < min_gold_required:
        return await m.reply("You need at least `500` gold to start mining.")
    success = random.choice([True, False])
    gold: int = int((inp * random.choice(lis))/100)
    if success:  
        user.gold += gold  
        await m.reply(f"You've struck gold! Reward: `{gold}` gold.")
    else:
        user.gold -= gold 
        await m.reply(f"No luck this time, keep mining!, Lost: `{gold}` gold.")
    return await user.update()

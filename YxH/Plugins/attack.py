from pyrogram import Client, filters
from . import get_user, YxH
import time
import random

@Client.on_message(filters.command('attack'))
@YxH()
async def attack(_, m, u):
    if not u.clan_id:
        return await m.reply('You must be the part of any clan to attack.')
    if not m.reply_to_message:
        return await m.reply('Reply to an user to attack.')
    t = await get_user(m.reply_to_message.from_user.id)
    if u.gold < 10000000:
        return await m.reply(f'You need `{10000000-u.gold}` more gold to attack.')
    u.gold -= 10000000
    if t.shield:
        if int(time.time()-t.shield[1]) > t.shield[0]:
            t.shield = []
    if t.shield:
        await u.update()
        return await m.reply('Oops, target user having shield equipped.')
    gold_per = random.randint(5, 10)
    gems_per = random.randint(5, 10)
    gold_val = int(t.gold * gold_per / 100)
    gems_val = int(t.gems * gems_per / 100)
    t.gold -= gold_val
    t.gems -= gems_val
    u.gold += gold_val
    u.gems += gems_val
    t.latest_defend = time.time()
    await u.update()
    await t.update()
    await m.reply(f'You\'ve looted `{gold_val}` Gold and `{gems_val}` Gems from **{t.user.first_name}**.')
    await _.send_message(t.user.id, f'You got attacked by **{u.user.first_name}**\n\nLost `{gold_val}` Gold and `{gems_val}` Gems.')
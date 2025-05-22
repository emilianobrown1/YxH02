from pyrogram import Client, filters
from . import get_user, YxH
from ..Database.attacks import increment_attack
import time
import random

@Client.on_message(filters.command('attack'))
@YxH()
async def attack(_, m, u):
    if not u.clan_id:
        return await m.reply('You must be part of a clan to attack.')

    # Determine target: via reply or /attack <user_id>
    if m.reply_to_message:
        target_user_id = m.reply_to_message.from_user.id
    else:
        parts = m.text.strip().split()
        if len(parts) < 2 or not parts[1].isdigit():
            return await m.reply('Usage: reply to a user with /attack or `/attack <user_id>`')
        target_user_id = int(parts[1])

    # Fetch target
    t = await get_user(target_user_id)

    if not t.clan_id:
        return await m.reply("You can only attack users who are part of a clan.")

    if u.clan_id == t.clan_id:
        return await m.reply("You cannot attack your clan mates.")

    if u.gold < 10_000_000:
        return await m.reply(f'You need `{10_000_000 - u.gold}` more gold to attack.')

    u.gold -= 10_000_000

    if t.shield:
        duration, start = t.shield
        if time.time() - start > duration:
            t.shield = []
    if t.shield:
        await u.update()
        return await m.reply('Oops, target user has a shield equipped.')

    if t.latest_defend and (time.time() - t.latest_defend) <= 10800:
        return await m.reply("Target was attacked recently; try again later.")

    gold_val = int(t.gold * random.randint(5, 10) / 100)
    gems_val = int(t.gems * random.randint(5, 10) / 100)

    t.gold -= gold_val
    t.gems -= gems_val
    u.gold += gold_val
    u.gems += gems_val
    t.latest_defend = time.time()

    await u.update()
    await t.update()

    # Update attack count and name
    await increment_attack(user_id=m.from_user.id, name=m.from_user.first_name)

    await m.reply(
        f'You\'ve looted `{gold_val}` Gold and `{gems_val}` Gems from **{t.user.first_name}**.'
    )
    await _.send_message(
        t.user.id,
        f'You got attacked by **{u.user.first_name}**\n\n'
        f'Lost `{gold_val}` Gold and `{gems_val}` Gems.'
    )
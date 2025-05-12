from pyrogram import Client, filters
from . import get_user, YxH, db
import time
import random

@Client.on_message(filters.command('attack'))
@YxH()
async def attack(_, m, u):
    if not u.clan_id:
        return await m.reply('You must be part of a clan to attack.')

    # Determine target: via reply or /attack <user_id>
    target_user_id = None
    if m.reply_to_message:
        target_user_id = m.reply_to_message.from_user.id
    else:
        parts = m.text.strip().split()
        if len(parts) >= 2 and parts[1].isdigit():
            target_user_id = int(parts[1])
        else:
            return await m.reply('Usage: reply to a user with /attack or `/attack <user_id>`')

    # Fetch target
    t = await get_user(target_user_id)

    if u.clan_id == t.clan_id:
        return await m.reply("You cannot attack your clan mates.")

    if u.gold < 10_000_000:
        needed = 10_000_000 - u.gold
        return await m.reply(f'You need `{needed}` more gold to attack.')

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

    gold_per = random.randint(5, 10)
    gems_per = random.randint(5, 10)
    gold_val = int(t.gold * gold_per / 100)
    gems_val = int(t.gems * gems_per / 100)

    t.gold -= gold_val
    t.gems -= gems_val
    u.gold += gold_val
    u.gems += gems_val
    t.latest_defend = time.time()

    # Save both users
    await u.update()
    await t.update()

    # Track attack in db.attacks for leaderboard
    user_id = m.from_user.id
    name = m.from_user.first_name
    await db.attacks.update_one(
        {"user_id": user_id},
        {"$set": {"name": name}, "$inc": {"attack": 1}},
        upsert=True
    )

    # Notify both users
    await m.reply(
        f'You\'ve looted `{gold_val}` Gold and `{gems_val}` Gems from **{t.user.first_name}**.'
    )
    await _.send_message(
        t.user.id,
        f'You got attacked by **{u.user.first_name}**\n\n'
        f'Lost `{gold_val}` Gold and `{gems_val}` Gems.'
    )
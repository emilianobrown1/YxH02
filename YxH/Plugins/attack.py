from pyrogram import Client, filters
from . import get_user, YxH
from . import YxH, db
import time
import random

@Client.on_message(filters.command('attack'))
@YxH()
async def attack(_, m, u):
    # Must be in a clan
    if not u.clan_id:
        return await m.reply('You must be part of a clan to attack.')
    
    # Determine target: either via reply or via /attack <user_id>
    target_user_id = None
    if m.reply_to_message:
        target_user_id = m.reply_to_message.from_user.id
    else:
        parts = m.text.strip().split()
        if len(parts) >= 2 and parts[1].isdigit():
            target_user_id = int(parts[1])
        else:
            return await m.reply('Usage: reply to a user with /attack or `/attack <user_id>`')
    
    # Fetch target user data
    t = await get_user(target_user_id)
    
    # Cannot attack your own clan
    if u.clan_id == t.clan_id:
        return await m.reply("You cannot attack your clan mates.")
    
    # Require 10M gold to initiate attack
    if u.gold < 10_000_000:
        needed = 10_000_000 - u.gold
        return await m.reply(f'You need `{needed}` more gold to attack.')
    
    # Deduct attack fee
    u.gold -= 10_000_000

    # Check and expire target’s shield
    if t.shield:
        duration, start = t.shield
        if time.time() - start > duration:
            t.shield = []
    if t.shield:
        await u.update()
        return await m.reply('Oops, target user has a shield equipped.')

    # Prevent rapid repeated attacks
    if t.latest_defend and (time.time() - t.latest_defend) <= 10800:
        return await m.reply("Target was attacked recently; try again later.")
    
    # Calculate loot percentages
    gold_per  = random.randint(5, 10)
    gems_per  = random.randint(5, 10)
    gold_val  = int(t.gold  * gold_per / 100)
    gems_val  = int(t.gems  * gems_per / 100)
    
    # Transfer loot
    t.gold   -= gold_val
    t.gems   -= gems_val
    u.gold   += gold_val
    u.gems   += gems_val
    t.latest_defend = time.time()
    
    # Persist changes
    await u.update()
    await t.update()
    
    # Notify attacker and target
    await m.reply(
        f'You\'ve looted `{gold_val}` Gold and `{gems_val}` Gems from **{t.user.first_name}**.'
    )
    await _.send_message(
        t.user.id,
        f'You got attacked by **{u.user.first_name}**\n\n'
        f'Lost `{gold_val}` Gold and `{gems_val}` Gems.'
    )



@Client.on_message(filters.command("attack"))
@YxH()
async def attack_handler(_, m, u):
    user_id = m.from_user.id
    name = m.from_user.first_name

    # Save or update attack data
    await db.attacks.update_one(
        {"user_id": user_id},
        {
            "$set": {"name": name},
            "$inc": {"attack": 1}
        },
        upsert=True
    )

    await m.reply("Attack executed! Your attack count has increased.")
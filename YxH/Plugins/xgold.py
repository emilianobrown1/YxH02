from pyrogram import Client, filters
from . import YxH, get_user

@Client.on_message(filters.command("xgold"))
@YxH(private=False, min_old=3)
async def xgold(_, m, u):
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply("Reply to an user to share gold with.")
    try:
        gold = m.text.split()[1]
        if gold == "*":
            gold = u.gold
        else:
            gold = int(gold)
    except:
        return await m.reply("Usage: /xgold [gold_amount]")
    if u.gold < gold:
        return await m.reply(f"⚠️ You having `{u.gold}` Gold.")
    t = await get_user(m.reply_to_message.from_user.id)
    if not t:
        return await m.reply("Replied user is not a player.")
    u.gold -= gold
    t.gold += gold
    await u.update()
    await t.update()
    await m.reply(f"You have paid `{gold}` Gold to **{t.user.first_name}**.")

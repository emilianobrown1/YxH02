from pyrogram import Client, filters
from . import YxH, get_date, get_week

@Client.on_message(filters.command("claim"))
@YxH()
async def claim(_, m, user):
  date, week = get_date(), get_week()
  l = [date, week]
  if user.bonus == l:
    return await m.reply("You have already claimed your bonus.")
  if user.bonus[1] != week:
    await m.reply("Weekly Bonus has been claimed: 550000 gems, 50000 gold, and 1 crystal")
    user.gems += 550000
    user.bonus = l
    return await user.update()
  if user.bonus[0] != date:
    await m.reply("Daily Bonus has been claimed, 50000")
    user.gems += 50000
    user.bonus = l
    return await user.update()
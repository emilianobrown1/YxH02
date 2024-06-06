from pyrogram import Client, filters
from ..Class.clan import Clan
from ..Database.clan import get_clan, get_clans_count
from ..Database.users import get_user
from ..universal_decorator import YxH
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb

temp = """
🏰 Clan Information 🏰

Clan: **{}**
Level: `{}`
Leader: **{}**
Members: `{}/15`

Join our mighty clan and conquer the fantasy world together! 💪🌟
"""

@Client.on_message(filters.command("clan"))
@YxH()
async def c(_, m, u):
  if not u.clan_id:
    return await m.reply("You are not placed in any clan, You can join a clan or create one using /create.")
  clan = await get_clan(u.clan_id)
  markup = [[ikb("Members", callback_data=f"members_{u.user.id}")]]
  if u.user.id == clan.leader:
    markup.append([ikb("Settings", callback_data=f"settings_{u.user.id}")])
  else:
    markup.append([ikb("Leave", callback_data=f"leave_{u.user.id}")])
  markup.append([ikb("Clan Link", url=f"https://t.me/{_.myself.username}?start=join_{clan.clan_id}")])
  leader = await get_user(clan.leader)
  txt = temp.format(clan.name, clan.level, leader.user.first_name, len(clan.members))
  return await m.reply(txt, reply_markup=ikm(markup))

@Client.on_message(filters.command("create"))
@YxH()
async def cr(_, m, u):
  if u.clan_id:
    return
  try:
    clan_name = "".join(m.text.split()[1:])
  except:
    return await m.reply("Usage: /create <clan name>")
  if u.crystals < 500:
    return await m.reply(f"You need `{500-u.crystals}` more crystal(s) to create a clan.")
  u.crystals -= 500
  clan_id = await get_clans_count() + 1
  u.clan_id = clan_id
  cl = Clan(clan_id, clan_name, u.user.id)
  ma = ikm([[ikb("Clan Link", url=f"https://t.me/{_.myself.username}?start=join_{clan_id}")]])
  await cl.update()
  await u.update()
  return await m.reply(f"(**{clan_name}**) Clan has been created.", reply_markup=ma)
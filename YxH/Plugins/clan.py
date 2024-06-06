from pyrogram import Client, filters
from ..Class.clan import Clan
from ..Database.clan import get_clan, get_clans_count
from ..universal_decorator import YxH

@Client.on_message(filters.command("clan"))
@YxH()
async def c(_, m, u):
    if not u.clan_id:
        return await m.reply("You are not placed in any clan, You can join a clan or create one using /create.")
    
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
  await cl.update()
  await u.update()
  return await m.reply(f"(**{clan_name}**) Clan has been created.")
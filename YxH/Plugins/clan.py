from pyrogram import Client, filters
from ..Class.clan import Clan
from ..Database.clan import get_clan
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
   
from pyrogram import Client, filters
from ..Class.clan import Clan
from ..universal_decorator import YxH

@Client.on_message(filters.command("clan"))
@YxH()
async def c(_, m, u):
    if not u.clan:
        return await m.reply("You are not placed in any clan, You can join a clan or create one using /create.")
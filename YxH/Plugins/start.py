from pyrogram import Client, filters
from ..Class import User
from ..Utils.strings import start_text
from ..Utils.markups import start_markup
from ..Database.users import get_user
from ..Database.clan import get_clan
from .clan import clan_info

@Client.on_message(filters.command("start") & filters.private)
async def start(_, m):
  user = await get_user(m.from_user.id)
  if "clan_" in m.text:
      txt, markup = await clan_info(await get_clan(int(m.text.split("_")[1])), m.from_user.id)
      return await m.reply(txt, reply_markup=markup)
  await m.reply_photo("Images/start.JPG", start_text.format(m.from_user.first_name), reply_markup=await start_markup())
  if not user:
    u = User(m.from_user)
    await u.update()
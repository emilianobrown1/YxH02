from pyrogram import Client, filters
from ..Class import User
from ..Utils.strings import start_text
from ..Utils.markups import start_markup
from ..Database.users import get_user
from .clan import join_clan

@Client.on_message(filters.command("start") & filters.private)
async def start(_, m):
  user = await get_user(m.from_user.id)
  if "join_" in m.text:
      return await join_clan(_, m, user)
  await m.reply_photo("Images/start.JPG", start_text.format(m.from_user.first_name), reply_markup=await start_markup())
  if not user:
    u = User(m.from_user)
    await u.update()
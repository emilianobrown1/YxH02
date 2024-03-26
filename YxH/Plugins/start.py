from pyrogram import Client, filters
from ..Class import User
from ..Utils.strings import start_text
from ..Utils.markups import start_markup
from ..Database.users import get_user

@Client.on_message(filters.command("start") & filters.private)
async def start(_, m):
  await m.reply_photo("Images/start.JPG", start_text, reply_markup=start_markup)
  user = m.from_user
  if not await get_user(user.id):
    u = User(user)
    await u.update()

from .watchers import user_watcher
from pyrogram import Client, filters
from . import get_user

@Client.on_message(filters.group, group=user_watcher)
async def cwf(_, m):
  u = await get_user(m.from_user.id)
  u.user = m.from_user
  await u.update()

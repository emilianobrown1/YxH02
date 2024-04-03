from .watchers import user_watcher
from . import Client, filters, get_user

@Client.on_message(group=user_watcher, filters.group)
async def cwf(_, m):
  u = await get_user(m.from_user.id)
  u.user = m.from_user
  await u.update()

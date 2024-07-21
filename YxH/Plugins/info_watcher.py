from .watchers import info_watcher
from . import get_user, get_chat
from ..Class.wordle import wordle
from ..Class import Chat
import asyncio

async def cwf(_, m):
  u, c = await asyncio.gather(
    get_user(m.from_user.id),
    get_chat(m.chat.id)
  )
  if u:
    u.user = m.from_user
    await asyncio.gather(
      u.update(),
    )
  if m.chat.id < 0:
    if c:
      c.chat = m.chat
    else:
      c: Chat = Chat(m.chat)
    await asyncio.gather(
      c.update(),
    )

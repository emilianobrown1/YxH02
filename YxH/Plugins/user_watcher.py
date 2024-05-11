from .watchers import info_watcher
from pyrogram import Client, filters
from . import get_user, get_chat
from ..load_attr import load_attr, load_chat_attr
from ..Class import Chat
import asyncio

@Client.on_message(filters.group, group=info_watcher)
async def cwf(_, m):
  u, c = await asyncio.gather(
    get_user(m.from_user.id),
    get_chat(m.chat.id)
  )
  if u:
    u.user = m.from_user
    await asyncio.gather(
      u.update(),
      load_attr(m.from_user.id)
    )
  if m.chat.id < 0:
    if c:
      c.chat = m.chat
    else:
      c: Chat = Chat(m.chat)
    await asyncio.gather(
      c.update(),
      load_chat_attr(m.chat.id)
    )
from pyrogram import Client, filters
from . import get_date, YxH, characters_count
import random

@Client.on_message(filters.command("superxshop"))
@YxH(private=False)
async def sxs(_, m, u):
  date = get_date()
  cc = await characters_count()
  if not date in u.store:
    store = []
    for i in range(1, cc+1):
      if len(store) == 3:
        break
      if not i in store:
        store.append(i)
    u.store = {date: store}
    await u.update()

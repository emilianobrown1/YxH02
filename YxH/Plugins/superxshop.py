from pyrogram import Client, filters
from . import get_date, YxH, characters_count
import random
from ..Utils.markups import store_markup
from ..Utils.templates import get_image_and_caption

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
  image, text = await get_image_and_caption(u.store[0])
  markup = store_markup(user_id, 1)
  await m.reply_photo(image, text, reply_markup=markup)

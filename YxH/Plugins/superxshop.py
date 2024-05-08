from pyrogram import Client, filters
from pyrogram.types import Message
from . import get_date, YxH, anime_characters_count
from ..Utils.markups import store_markup
from ..Utils.templates import get_anime_image_and_caption
from ..Class.user import User
import random

@Client.on_message(filters.command("superxshop"))
@YxH(private=False)
async def sxs(_, m: Message, u: User):
  date = get_date()
  cc = await anime_characters_count()
  all = list(range(1, cc+1))
  if not date in u.store:
    u.store_purchases = {date: [False, False, False]}
    store = []
    while len(store) != 3:
      r = random.choice(all)
      if r in store:
        continue
      store.append(r)
    u.store = {date: store}
    u.store_purchases = {date: [False, False, False]}
    await u.update()
  image, text = await get_anime_image_and_caption(u.store[date][0])
  markup = store_markup(u.user.id, 1, u.store_purchases[date][0])
  await m.reply_photo(image, caption=text, reply_markup=markup)

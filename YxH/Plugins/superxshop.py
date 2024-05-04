from pyrogram import Client, filters
from pyrogram.types import Message
from . import get_date, YxH, anime_characters_count
from ..Utils.markups import store_markup
from ..Utils.templates import get_anime_image_and_caption

@Client.on_message(filters.command("superxshop"))
@YxH(private=False)
async def sxs(_, m: Message, u):
  date = get_date()
  cc = await anime_characters_count()
  if not date in u.store:
    store = []
    for i in range(1, cc+1):
      if len(store) == 3:
        break
      if not i in store:
        store.append(i)
    u.store = {date: store}
    await u.update()
  image, text = await get_anime_image_and_caption(u.store[date][0])
  markup = store_markup(u.user.id, 1)
  await m.reply_photo(image, caption=text, reply_markup=markup)

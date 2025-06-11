from pyrogram import Client, filters
from pyrogram.types import Message
from . import get_date, YxH
from ..Utils.markups import store_markup
from ..Utils.templates import get_anime_image_and_caption
from ..Class.user import User
from ..Database.characters import get_anime_character_ids
import random

@Client.on_message(filters.command("superxshop"))
@YxH(private=False)
async def sxs(_, m: Message, u: User):
    date = get_date()

    # ✅ If store for today already exists, deny reopening
    if date in u.store:
        await m.reply("🛒 Your SuperXShop is already open. Please finish it before opening again.")
        return

    # 👇 Store not open yet: continue normal logic
    all = await get_anime_character_ids()
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
from pyrogram import Client, filters
from pyrogram.types import Message
from . import get_date, YxH
from ..Utils.markups import store_markup
from ..Utils.templates import get_anime_image_and_caption
from ..Class.user import User
from ..Database.characters import get_anime_character_ids
import random

# Memory store to keep track of users who already opened shop
active_shops = set()

@Client.on_message(filters.command("superxshop"))
@YxH(private=False)
async def sxs(_, m: Message, u: User):
    if u.user.id in active_shops:
        await m.reply("🛒 Your SuperXShop is already open. Please finish it before opening again.")
        return

    active_shops.add(u.user.id)  # Mark shop as active for the user

    date = get_date()
    all = await get_anime_character_ids()
    
    if date not in u.store:
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
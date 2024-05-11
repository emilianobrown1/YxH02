from pyrogram import Client, filters
from . import YxH, get_anime_character
from ..Utils.markups import acollection_markup
from ..Utils.templates import acollection_template
import asyncio
import math

@Client.on_message(filters.command('collection'))
@YxH()
async def collection(_, m, u):
    coll_dict: dict = u.collection
    if not coll_dict:
        return await m.reply('Your collection is empty.')
    total: int = math.ceil(len(coll_dict) / 5)
    first_5: list[int] = list(coll_dict)[:5]
    no_first_5: list[int] = list(coll_dict.values())[:5]
    first_5_obj = await asyncio.gather(*[asyncio.create_task(get_anime_character(i)) for i in first_5])
    first_5_dict: list[dict] = [i.__dict__ for i in first_5_obj]
    txt = f"{u.user.first_name}'s collection\n"
    txt += f'page: 1/{total}\n\n'
    txt += acollection_template(first_5_dict, no_first_5)
    markup = acollection_markup(1, u, first_5)
    image = (await get_anime_character(first_5[0])).image
    await m.reply_photo(image, caption=txt, reply_markup=markup)

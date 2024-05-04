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
    first_5_obj = asyncio.gather(*[asyncio.create_task(get_anime_character(i)) for i in first_5])
    first_5_dict: list[dict] = [i.__dict__ for i in first_5_obj]
    txt = f"{u.user.first_name}'s collection\n"
    txt += f'page: 1/{total}\n\n'
    txt += acollection_template(first_5_dict)
    markup = acollection_markup(total, 2, u)
    await m.reply(txt, reply_markup=markup)

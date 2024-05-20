from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from . import YxH, get_anime_character, get_user, get_chat
from ..Database.characters import get_anime_character_ids
from ..Utils.templates import copx_template

import asyncio
import random

count: dict[int, int] = {}

def markup(id: int) -> ikm:
    return ikm([[ikb('Name', callback_data=f'name{id}')]])

async def cwf(_, m):
    global count
    try:
        user_id = m.from_user.id
        chat_id = m.chat.id
        user, chat = await asyncio.gather(
            get_user(user_id),
            get_chat(chat_id)
        )
    except:
        return
    if user.blocked:
        return
    if chat_id in count:
        count[chat_id] += 1
    else:
        count[chat_id] = 1
    if count[chat_id] == chat.copx_cooldown:
        ids = await get_anime_character_ids()
        id = random.choice(ids)
        chat.copx_status = id
        await chat.update()
        info = await get_anime_character(id)
        info = info.__dict__
        cap: str = copx_template(info)
        im: str = info['image']
        await _.send_photo(chat_id, im, caption=cap, reply_markup=markup(id))
        count[chat_id] = 0

@Client.on_message(filters.command('copx'))
@YxH(private=False)
async def copx(_, m, u):
    chat = await get_chat(m.chat.id)
    user = u
    char = chat.copx_status
    if char == 0:
        return
    info = (await get_anime_character(char)).__dict__
    text_spl = m.text.split()[1:]
    if len(text_spl) == 0:
        return
    name = info['name'].lower().split()
    for x in text_spl:
        if not x.lower() in name:
            return
    if user.gems < info['price']:
        return await m.reply('Sed, no enuf gems.')
    user.gems -= info['price']
    if char in user.collection:
        user.collection[char] += 1
    else:
        user.collection[char] = 1
    chat.copx_status = 0
    await asyncio.gather(
        chat.update(),
        user.update(),
        m.reply(f'{m.from_user.first_name}, you have successfully bought {info["name"]} for {info["price"]} gems.')
    )
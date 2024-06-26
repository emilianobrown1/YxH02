from ..Database.characters import get_all
from ..Database.users import get_user
from pyrogram import Client, filters
from pyrogram.types import InlineQuery
import asyncio
from ..universal_decorator import YxH
from . import ikm, ikb

answers = {}
names = {}

async def load():
    global answers, names
    all = await get_all()
    all = all.values()
    new = {x.id: x.inline for x in all if hasattr(x, 'inline')}
    answers = new
    xd = {}
    for x in all:
        if x.name.lower() in xd:
            xd[x.name.lower()].append(x.id)
        else:
            xd[x.name.lower()] = [x.id]
        if x.anime.lower() in xd:
            xd[x.anime.lower()].append(x.id)
        else:
            xd[x.anime.lower()] = [x.id]
    names = xd
    
@Client.on_message(filters.command("inline"))
@YxH()
async def inl_short_button(_, m, u):
    markup = ikm([[ikb("Inline", switch_inline_query_current_chat="")]])
    return await m.reply("Inline", reply_markup=markup)
        
@Client.on_message(filters.command("reload"))
@YxH(sudo=True)
async def loads(_, m, u):
    msg = await m.reply("Reloading...")
    await load()
    await msg.edit("Reloaded.")

@Client.on_inline_query()
async def inl(_, i: InlineQuery):
    final_answers = []
    if i.query.startswith("view"):
        ids = list(map(int, i.query.split("|")[1:]))
        final_answers = [answers[y] for y in ids]
    if i.query.startswith("collection_"):
        try:
            user_id = int(i.query.split("_")[1])
        except:
            user_id = i.from_user.id
        user = await get_user(user_id)
        for x in user.collection:
            final_answers.append(answers[x])
    if i.query != "":
        try:
            ids = [int(i.query)]
        except:
            ids = []
            for x in names:
                if i.query.lower() in x:
                    ids += names[x]
        if ids:
            final_answers = [answers[y] for y in ids]
    else:
        final_answers = list(answers.values())
    offset = int(i.offset or 0)
    NEXT = 30
    if offset+NEXT > len(final_answers):
        hehe = len(final_answers)
    else:
        hehe = offset+NEXT
    images = final_answers[offset: hehe]
    await i.answer(results=images, is_gallery=True, cache_time=1, next_offset=str(offset + NEXT))

asyncio.create_task(load())
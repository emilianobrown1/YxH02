from ..Database.characters import get_all
from ..Database.users import get_user
from pyrogram import Client, filters
from pyrogram.types import InlineQuery
import asyncio
from ..universal_decorator import YxH

answers = {}

async def load():
    global answers
    if not answers:
        all = await get_all()
        new = {x.id: x.inline for x in all.values() if hasattr(x, 'inline')}
        answers = new
        
@Client.on_message(filters.command("reload"))
@YxH(sudo=True)
async def loads(_, m, u):
    msg = await m.reply("Reloading...")
    await load()
    await msg.edit("Reloaded.")

@Client.on_inline_query()
async def inl(_, i: InlineQuery):
    if i.query.startswith("collection_"):
        try:
            user_id = int(i.query.split("_")[1])
        except:
            user_id = i.from_user.id
        user = await get_user(user_id)
        final_answers = []
        for x in user.collection:
            final_answers.append(answers[x])
    else:
        final_answers = answers
    offset = int(i.offset or 0)
    NEXT = 30
    if offset+NEXT > len(final_answers):
        hehe = len(final_answers)
    else:
        hehe = offset+NEXT
    images = final_answers[offset: hehe]
    await i.answer(results=images, is_gallery=True, cache_time=1, next_offset=str(offset + NEXT))

asyncio.create_task(load())
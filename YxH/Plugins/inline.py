from ..Database.characters import get_all
from pyrogram import Client, filters
from pyrogram.types import InlineQuery
import asyncio

answers = []

async def load():
    global answers
    if not answers:
        all = await get_all()
        new = [x.inline for x in all.values() if hasattr(x, 'inline')]
        answers = new

@Client.on_inline_query()
async def inl(_, i: InlineQuery):
    offset = int(i.offset or 0)
    NEXT = 30
    images = answers[offset: offset+NEXT]
    await i.answer(results=images, is_gallery=True, cache_time=1, next_offset=str(offset + NEXT))

asyncio.create_task(load())
from ..Database.users import get_all_users
from ..Database.clan import get_clans
from wordle import time_out_func
from ..Database.chats import get_all_chats
from ..load_attr import load_attr, load_clan_attr, load_chat_attr
import asyncio

async def func():
    users = await get_all_users()
    tasks = []
    for x in users:
        tasks.append(asyncio.create_task(load_attr(x)))
    await asyncio.gather(*tasks)
    users = await get_all_chats()
    tasks = []
    for x in users:
        tasks.append(asyncio.create_task(load_chat_attr(x)))
    await asyncio.gather(*tasks)
    users = await get_clans()
    tasks = []
    for x in users:
        tasks.append(asyncio.create_task(load_clan_attr(x)))
    await asyncio.gather(*tasks)

asyncio.create_task(func())
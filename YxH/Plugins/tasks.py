from ..Database.users import get_all_users
from ..load_attr import load_attr, load_clan_attr, load_chat_attr
import asyncio

async def func():
    users = await get_all_users()
    tasks = []
    for x in users:
        tasks.append(asyncio.create_task(load_attr(x.user.id)))
    await asyncio.gather(*tasks)

asyncio.create_task(func())
import asyncio

from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

mongo = MongoClient(MONGO_DB_URI)
db = mongo.YxH


async def func():
    print(await db.users.find_one({'user_id': 5903688119}))
    await db.users.delete_one({'user_id': 5903688119})

asyncio.run(func())
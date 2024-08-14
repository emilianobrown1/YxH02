import asyncio
import pickle

from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

mongo = MongoClient(MONGO_DB_URI)
db = mongo.YxH

test_user: int = 1086394021

async def func():
    user = await db.users.find_one({'user_id': test_user})
    # print(user)
    user = pickle.loads(user['info'])
    user.collection = {1: 3}
    await user.update()

asyncio.run(func())
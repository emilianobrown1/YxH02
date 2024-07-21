from . import db
import pickle
import time
from datetime import datetime

udb = db.users
adb = db.wordle
cdb = db.wordle_avg
ldb = db.wordle_limit

def today():
    return datetime.now().strftime("%Y-%m-%d")

async def add_game(user_id: int):
    user_id = str(user_id)
    x = await adb.find_one({"_": "_"})
    if x:
        dic = x['dic']
    else:
        dic = {}
    if user_id in dic:
        dic[user_id] = str(int(dic[user_id]) + 1)
    else:
        dic[user_id] = '1'
    await adb.update_one({"_": "_"}, {"$set": {"dic": dic}}, upsert=True)

async def get_wordle_dic():
    x = await adb.find_one({"_": "_"})
    if x:
        return x['dic']
    return {}

async def add(user_id: int, guesses: int):
    x = await cdb.find_one({"user_id": user_id})
    if x:
        lis = x['lis']
    else:
        lis = []
    lis.append(guesses)
    await cdb.update_one({"user_id": user_id}, {"$set": {"lis": lis}}, upsert=True)

async def get_avg(user_id: int):
    x = await cdb.find_one({"user_id": user_id})
    if x:
        lis = x['lis']
    else:
        lis = []
    total = sum(lis)
    count = len(lis)
    return total / count if count > 0 else 0

async def incr_game(user_id: int):
    td = today()
    x = await ldb.find_one({"user_id": user_id})
    if x:
        dic = x["dic"]
        dic[td] = dic.get(td, 0) + 1
    else:
        dic = {td: 1}
    await ldb.update_one({"user_id": user_id}, {"$set": {"dic": dic}}, upsert=True)

async def get_today_games(user_id: int):
    td = today()
    x = await ldb.find_one({"user_id": user_id})
    if x:
        dic = x["dic"]
        return dic.get(td, 0)
    return 0

async def get_all_games(user_id: int):
    x = await ldb.find_one({"user_id": user_id})
    if x:
        return x["dic"]
    return {}

async def add_crystal(user_id: int, crystals: int):
    user_data = await udb.find_one({"user_id": user_id})
    if user_data:
        user_info = pickle.loads(user_data['info'])
        user_info.crystals += crystals
        await udb.update_one({"user_id": user_id}, {"$set": {"info": pickle.dumps(user_info)}})
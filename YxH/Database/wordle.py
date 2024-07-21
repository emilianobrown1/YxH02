from . import db
import pickle
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
    dic = x['dic'] if x else {}
    dic[user_id] = str(int(dic.get(user_id, '0')) + 1)
    await adb.update_one({"_": "_"}, {"$set": {"dic": dic}}, upsert=True)

async def get_wordle_dic():
    x = await adb.find_one({"_": "_"})
    return x['dic'] if x else {}

async def add(user_id: int, guesses: int):
    user_id = str(user_id)
    x = await cdb.find_one({"user_id": user_id})
    lis = x['lis'] if x else []
    lis.append(guesses)
    await cdb.update_one({"user_id": user_id}, {"$set": {"lis": lis}}, upsert=True)

async def get_avg(user_id: int):
    user_id = str(user_id)
    x = await cdb.find_one({"user_id": user_id})
    lis = x['lis'] if x else []
    total = sum(lis)
    count = len(lis)
    return total / count if count > 0 else 0

async def incr_game(user_id: int):
    user_id = str(user_id)
    td = today()
    x = await ldb.find_one({"user_id": user_id})
    dic = x["dic"] if x else {}
    dic[td] = dic.get(td, 0) + 1
    await ldb.update_one({"user_id": user_id}, {"$set": {"dic": dic}}, upsert=True)

async def get_today_games(user_id: int):
    user_id = str(user_id)
    td = today()
    x = await ldb.find_one({"user_id": user_id})
    dic = x["dic"] if x else {}
    return dic.get(td, 0)

async def get_all_games(user_id: int):
    user_id = str(user_id)
    x = await ldb.find_one({"user_id": user_id})
    return x["dic"] if x else {}

async def add_crystal(user_id: int, crystals: int):
    user_id = str(user_id)
    user_data = await udb.find_one({"user_id": user_id})
    if user_data:
        user_info = pickle.loads(user_data['info'])
        user_info.crystals += crystals
        await udb.update_one({"user_id": user_id}, {"$set": {"info": pickle.dumps(user_info)}})
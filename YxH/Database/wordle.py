from . import db
import pickle 
import time
from datetime import datetime
from ..Class.user import wordle

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
    sum = 0
    a = 0
    for y in lis:
        sum += y
        a += 1
    if a == 0:
        return 0
    return sum / a

async def incr_game(user_id: int):
    td = today()
    x = await ldb.find_one({"user_id": user_id})
    if x:
        dic = x["dic"]
        if td in dic:
            dic[td] += 1
        else:
            dic[td] = 1
    else:
        dic = {td: 1}
    await ldb.update_one({"user_id": user_id}, {"$set": {"dic": dic}}, upsert=True)

async def get_today_games(user_id: int):
    td = today()
    x = await ldb.find_one({"user_id": user_id})
    if x:
        dic = x["dic"]
        if td in dic:
            return dic[td]
        return 0
    return 0

async def get_all_games(user_id: int):
    x = await ldb.find_one({"user_id": user_id})
    if x:
        return x["dic"]
    return {}

async def add_crystal(user_id: int, crystals: int):
    user = wordle(user_id)
    await user.add_crystals(crystals)

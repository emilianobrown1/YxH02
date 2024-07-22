from . import db
import pickle
from datetime import datetime

adb = db.wordle
cdb = db.wordle_avg
ldb = db.wordle_limit
udb = db.users

async def add_game(user_id: int):
    user_id = str(user_id)
    await adb.update_one(
        {"_": "_"},
        {"$inc": {f"dic.{user_id}": 1}},
        upsert=True
    )

async def get_wordle_dic():
    result = await adb.find_one({"_": "_"})
    return result.get('dic', {}) if result else {}

async def add(user_id: int, guesses: int):
    user_id = str(user_id)
    await cdb.update_one(
        {"user_id": user_id},
        {"$push": {"lis": guesses}},
        upsert=True
    )

async def get_avg(user_id: int):
    user_id = str(user_id)
    result = await cdb.find_one({"user_id": user_id})
    if result and 'lis' in result:
        lis = result['lis']
        return sum(lis) / len(lis) if lis else 0
    return 0

async def incr_game(user_id: int):
    user_id = str(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    await ldb.update_one(
        {"user_id": user_id},
        {"$inc": {f"dic.{today}": 1}},
        upsert=True
    )

async def get_today_games(user_id: int):
    user_id = str(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    result = await ldb.find_one({"user_id": user_id})
    return result['dic'].get(today, 0) if result and 'dic' in result else 0

async def add_crystal(user_id: int, crystals: int):
    user_id = str(user_id)
    user_data = await udb.find_one({'user_id': user_id})
    if user_data:
        user_info = pickle.loads(user_data['info'])
        user_info.crystals += crystals
        await udb.update_one(
            {'user_id': user_id},
            {'$set': {'info': pickle.dumps(user_info)}}
        )

async def get_all_wordle_users():
    cursor = adb.find({"_": "_"})
    result = await cursor.to_list(length=None)
    return result[0]['dic'] if result else {}

async def get_user_wordle_data(user_id: int):
    user_id = str(user_id)
    avg_data = await cdb.find_one({"user_id": user_id})
    limit_data = await ldb.find_one({"user_id": user_id})
    return {
        'average': avg_data.get('lis', []) if avg_data else [],
        'daily_games': limit_data.get('dic', {}) if limit_data else {}
    }
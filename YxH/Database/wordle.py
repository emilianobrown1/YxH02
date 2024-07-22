from . import db
from datetime import datetime

adb = db.wordle
cdb = db.wordle_avg
ldb = db.wordle_limit

async def add_game(user_id: int) -> None:
    user_id = str(user_id)
    await adb.update_one(
        {"_": "_"},
        {"$inc": {f"dic.{user_id}": 1}},
        upsert=True
    )

async def get_wordle_dic() -> dict:
    result = await adb.find_one({"_": "_"})
    return result.get('dic', {}) if result else {}

async def add(user_id: int, guesses: int) -> None:
    user_id = str(user_id)
    await cdb.update_one(
        {"user_id": user_id},
        {"$push": {"lis": guesses}},
        upsert=True
    )

async def get_avg(user_id: int) -> float:
    user_id = str(user_id)
    result = await cdb.find_one({"user_id": user_id})
    if result and 'lis' in result:
        lis = result['lis']
        return sum(lis) / len(lis) if lis else 0
    return 0.0

async def incr_game(user_id: int) -> None:
    user_id = str(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    await ldb.update_one(
        {"user_id": user_id},
        {"$inc": {f"dic.{today}": 1}},
        upsert=True
    )

async def get_today_games(user_id: int) -> int:
    user_id = str(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    result = await ldb.find_one({"user_id": user_id})
    return result['dic'].get(today, 0) if result else 0

async def add_crystal(user_id: int, crystals: int) -> None:
    user_id = str(user_id)
    await db.users.update_one(
        {"user_id": user_id},
        {"$inc": {"crystals": crystals}}
    )
from . import db
import pickle
import time
from datetime import datetime

udb = db.users
adb = db.wordle  # Stores total games per user
cdb = db.wordle_avg  # Stores individual guess history for averages
ldb = db.wordle_limit  # Tracks daily game limits

def today():
    return datetime.now().strftime("%Y-%m-%d")

async def add_game(user_id: int):
    user_id_str = str(user_id)
    # Find the document with _id "total_games" which holds all users' game counts
    doc = await adb.find_one({"_id": "total_games"})
    if doc:
        user_games = doc.get("games", {})
        current_count = int(user_games.get(user_id_str, 0))
        user_games[user_id_str] = current_count + 1
    else:
        user_games = {user_id_str: 1}
    # Update or insert the document with _id "total_games"
    await adb.update_one(
        {"_id": "total_games"},
        {"$set": {"games": user_games}},
        upsert=True
    )

async def get_wordle_dic():
    doc = await adb.find_one({"_id": "total_games"})
    return doc.get("games", {}) if doc else {}

async def add(user_id: int, guesses: int):
    # Append the guess count to the user's list in wordle_avg
    await cdb.update_one(
        {"user_id": user_id},
        {"$push": {"lis": guesses}},
        upsert=True
    )

async def get_avg(user_id: int):
    doc = await cdb.find_one({"user_id": user_id})
    if not doc or not doc.get("lis"):
        return 0
    guesses = doc["lis"]
    return sum(guesses) / len(guesses)

async def incr_game(user_id: int):
    td = today()
    # Increment daily game count for the user
    await ldb.update_one(
        {"user_id": user_id},
        {"$inc": {f"daily.{td}": 1}},
        upsert=True
    )

async def get_today_games(user_id: int):
    td = today()
    doc = await ldb.find_one({"user_id": user_id})
    if doc:
        return doc.get("daily", {}).get(td, 0)
    return 0

# Note: The add_crystal function might be redundant if handled by User class
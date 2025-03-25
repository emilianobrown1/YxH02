from . import db

async def save_quest_data(user_id, quest_data):
    await db.quests.update_one(
        {"user_id": user_id},
        {"$set": {"quest_data": quest_data}},
        upsert=True
    )

async def get_quest_data(user_id):
    user_data = await db.quests.find_one({"user_id": user_id})
    return user_data.get("quest_data") if user_data else None

async def delete_quest_data(user_id):
    await db.quests.delete_one({"user_id": user_id})
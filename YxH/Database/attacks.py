from . import db

attack_col = db.attacks  # This will create/use a collection called "attacks"

async def increment_attack(user_id: int):
    await attack_col.update_one(
        {"user_id": user_id},
        {"$inc": {"attack": 1}},
        upsert=True
    )

async def increment_comboattack(user_id: int):
    await attack_col.update_one(
        {"user_id": user_id},
        {"$inc": {"comboattack": 1}},
        upsert=True
    )

async def get_top_attackers(limit=10):
    cursor = attack_col.find().sort([("attack", -1), ("comboattack", -1)]).limit(limit)
    return await cursor.to_list(length=limit)

async def get_user_attacks(user_id: int):
    return await attack_col.find_one({"user_id": user_id}) or {"attack": 0, "comboattack": 0}

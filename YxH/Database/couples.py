from . import db

couples_db = db.couples
couple_chat_messages = db.couple_chat_messages  # New collection for message tracking

async def add_couple(user1_id, user2_id):
    """Add a couple to the database."""
    await couples_db.insert_one({"user1": user1_id, "user2": user2_id, "message_count": 0})

async def get_partner(user_id):
    """Retrieve the partner of a user."""
    couple = await couples_db.find_one({"user1": user_id}) or await couples_db.find_one({"user2": user_id})
    if couple:
        return couple["user2"] if couple["user1"] == user_id else couple["user1"]
    return None

async def remove_couple(user_id):
    """Remove a couple and their chat messages."""
    couple = await couples_db.find_one({"user1": user_id}) or await couples_db.find_one({"user2": user_id})
    if couple:
        user1 = couple["user1"]
        user2 = couple["user2"]
        await couples_db.delete_one({"_id": couple["_id"]})
        await couple_chat_messages.delete_many({"user1": user1, "user2": user2})

async def get_all_couples():
    """Retrieve all couples."""
    couples = await couples_db.find().to_list(length=None)
    return [(couple["user1"], couple["user2"]) for couple in couples]

async def get_couple(user_id):
    """Retrieve the couple document."""
    return await couples_db.find_one({"user1": user_id}) or await couples_db.find_one({"user2": user_id})

async def increment_couple_chat_messages(user1, user2, chat_id):
    """Increment message count and return the new count."""
    await couple_chat_messages.update_one(
        {"user1": user1, "user2": user2, "chat_id": chat_id},
        {"$inc": {"message_count": 1}},
        upsert=True
    )
    doc = await couple_chat_messages.find_one({"user1": user1, "user2": user2, "chat_id": chat_id})
    return doc.get("message_count", 0)
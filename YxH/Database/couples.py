from . import db

couples_db = db.couples  # A new collection for couples

async def add_couple(user1_id, user2_id):
    """Add a couple to the database."""
    await couples_db.insert_one({"user1": user1_id, "user2": user2_id})

async def get_partner(user_id):
    """Retrieve the partner of a user."""
    couple = await couples_db.find_one({"user1": user_id}) or await couples_db.find_one({"user2": user_id})
    if couple:
        return couple["user2"] if couple["user1"] == user_id else couple["user1"]
    return None

async def remove_couple(user_id):
    """Remove a couple from the database."""
    couple = await couples_db.find_one({"user1": user_id}) or await couples_db.find_one({"user2": user_id})
    if couple:
        await couples_db.delete_one({"_id": couple["_id"]})
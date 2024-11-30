from. import db
import pickle

async def add_couple(user1_id, user2_id):
    """Add a couple relationship between two users."""
    # Create or update couple relationship between user1 and user2
    await db.update_one(
        {"user1": user1_id}, {"$set": {"user2": user2_id}}, upsert=True
    )
    await db.update_one(
        {"user1": user2_id}, {"$set": {"user2": user1_id}}, upsert=True
    )

async def rmv_couple(user1_id, user2_id):
    """Remove a couple relationship between two users."""
    # Remove the couple relationship between user1 and user2
    await db.delete_one({"user1": user1_id, "user2": user2_id})
    await db.delete_one({"user1": user2_id, "user2": user1_id})

async def get_couple(user_id):
    """Retrieve the couple of a user."""
    # Find the couple of the given user
    couple = await db.find_one({"user1": user_id})
    if couple:
        return couple["user2"]
    # If not found with "user1", check "user2" as the other half
    couple = await db.find_one({"user2": user_id})
    if couple:
        return couple["user1"]
    return None

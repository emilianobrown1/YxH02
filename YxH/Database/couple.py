from . import db  # Assuming db is your MotorClient instance
from ..Database.users import get_user  # Ensure correct relative import
import pickle

async def add_couple(user1_id, user2_id):
    """Add a couple relationship between two users."""
    couple_collection = db.get_collection("couples")

    # Create the couple if it doesn't exist
    await couple_collection.update_one(
        {"user1": user1_id},
        {"$set": {"user2": user2_id, "message_gems": 0}},
        upsert=True
    )
    await couple_collection.update_one(
        {"user1": user2_id},
        {"$set": {"user2": user1_id, "message_gems": 0}},
        upsert=True
    )

async def rmv_couple(user1_id, user2_id):
    """Remove a couple relationship between two users."""
    couple_collection = db.get_collection("couples")
    
    # Delete both directions of the couple relationship
    await couple_collection.delete_one({"user1": user1_id, "user2": user2_id})
    await couple_collection.delete_one({"user1": user2_id, "user2": user1_id})

async def get_couple(user_id):
    """Retrieve the couple of a user."""
    couple_collection = db.get_collection("couples")
    
    # Find the couple associated with user1
    couple = await couple_collection.find_one({"user1": user_id})
    if couple:
        return couple["user2"]
    
    # If not found with "user1", check "user2" as the other half
    couple = await couple_collection.find_one({"user2": user_id})
    if couple:
        return couple["user1"]
    
    return None

async def add_message_gems(user1_id, user2_id, gems):
    """Add gems earned through messaging to the couple."""
    couple_collection = db.get_collection("couples")

    # Increment the gems earned for this couple in both directions
    await couple_collection.update_one(
        {"user1": user1_id, "user2": user2_id},
        {"$inc": {"message_gems": gems}},
        upsert=True
    )
    await couple_collection.update_one(
        {"user1": user2_id, "user2": user1_id},
        {"$inc": {"message_gems": gems}},
        upsert=True
    )

async def get_top_couples(limit=10):
    """
    Retrieve the top couples by total gems earned through messaging, with user names.
    """
    couple_collection = db.get_collection("couples")

    # Aggregation pipeline to sort and limit the top couples
    pipeline = [
        {"$sort": {"message_gems": -1}},  # Sort by 'message_gems' in descending order
        {"$limit": limit},  # Limit the results to the top 'limit'
        {"$project": {"user1": 1, "user2": 1, "message_gems": 1}},  # Project relevant fields
    ]

    top_couples = await couple_collection.aggregate(pipeline).to_list(length=limit)

    # Fetch user names for each couple
    for couple in top_couples:
        user1_data = await get_user(couple["user1"])  # Fetch user1 details
        user2_data = await get_user(couple["user2"])  # Fetch user2 details

        # Adjust attribute name to match your User class
        user1_name = getattr(user1_data, 'name', None) or f"User{couple['user1']}"
        user2_name = getattr(user2_data, 'name', None) or f"User{couple['user2']}"

        # Update couple dictionary with names
        couple["user1_name"] = user1_name
        couple["user2_name"] = user2_name

    return top_couples

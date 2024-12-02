from . import db  # Assuming db is your MotorClient instance
import pickle

async def add_couple(user1_id, user2_id):
    """Add a couple relationship between two users."""
    # Access the 'couples' collection and create or update couple relationship between user1 and user2
    couple_collection = db.get_collection("couples")
    
    # Update the couple relationship
    await couple_collection.update_one(
        {"user1": user1_id}, {"$set": {"user2": user2_id}}, upsert=True
    )
    await couple_collection.update_one(
        {"user1": user2_id}, {"$set": {"user2": user1_id}}, upsert=True
    )

async def rmv_couple(user1_id, user2_id):
    """Remove a couple relationship between two users."""
    # Access the 'couples' collection and remove the couple relationship
    couple_collection = db.get_collection("couples")
    
    # Delete both directions of the couple relationship
    await couple_collection.delete_one({"user1": user1_id, "user2": user2_id})
    await couple_collection.delete_one({"user1": user2_id, "user2": user1_id})

async def get_couple(user_id):
    """Retrieve the couple of a user."""
    # Access the 'couples' collection
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

    # Increment the gems earned for this couple
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
    Retrieve the top couples by total gems earned through messaging.
    """
    # Get the "couples" collection
    couple_collection = db.get_collection("couples")

    # Aggregation pipeline to sort and limit the top couples
    pipeline = [
        {"$sort": {"message_gems": -1}},  # Sort by 'message_gems' in descending order
        {"$limit": limit},  # Limit the results to the top 'limit'
        {"$project": {"user1": 1, "user2": 1, "message_gems": 1}},  # Project relevant fields
    ]

    # Execute the aggregation pipeline
    top_couples = await couple_collection.aggregate(pipeline).to_list(length=limit)
    return top_couples

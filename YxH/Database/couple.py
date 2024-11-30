from . import db
import pickle


db = db.couple  

async def add_couple(i, f):
    """Add a couple relationship between two users."""
    await db.update_one({"i": i}, {"$set": {"f": f}}, upsert=True)
    await db.update_one({"i": f}, {"$set": {"f": i}}, upsert=True)

async def rmv_couple(i, f):
    """Remove a couple relationship between two users."""
    await db.delete_one({"i": i})
    await db.delete_one({"i": f})

async def get_couple(i):
    """Retrieve the couple of a user."""
    x = await db.find_one({"i": i})
    if not x:
        return None
    return x["f"]

from . import db
import pickle

db = db.clan

async def get_clan(clan_id):
    x = await db.find_one({"clan_id": clan_id})
    if x:
        pickle.loads(return x["info"])
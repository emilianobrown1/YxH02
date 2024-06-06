from . import db
import pickle

db = db.clan

async def get_clan(clan_id):
    x = await db.find_one({"clan_id": clan_id})
    if x:
        pickle.loads(return x["info"])
        
async def get_clans_count() -> int:
    x = db.find()
    x = await x.to_list(length=None)
    return len(x)
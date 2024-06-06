from ..Database import db
import pickle

class Clan:
    def __init__(self, clan_id, owner):
        self.clan_id = clan_id
        self.owner = owner
        self.members = []
        
    async def update(self):
        await db.clan.update_one({"clan_id": self.clan_id}, {"$set": {"info": pickle.dumps(self)}}, upsert=True)
from ..Database.clan import db
import pickle

class Clan:
    def __init__(self, clan_id, clan_name, owner):
        self.clan_id = clan_id
        self.clan_name = clan_name
        self.owner = owner
        self.members = []
        
    async def update(self):
        await db.update_one({"clan_id": self.clan_id}, {"$set": {"info": pickle.dumps(self)}}, upsert=True)
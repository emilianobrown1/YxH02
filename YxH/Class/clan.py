from ..Database.clan import db
import pickle

class Clan:
    def __init__(self, clan_id, clan_name, leader):
        self.id = clan_id
        self.name = clan_name
        self.leader = leader
        self.members = []
        self.level = 1
        self.anyone_can_join = True
        self.join_requests = []
        
    async def update(self):
        await db.update_one({"clan_id": self.id}, {"$set": {"info": pickle.dumps(self)}}, upsert=True)
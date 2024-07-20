from ..Database.wordle import db
import time
from datetime import datetime
import pickle

class wordle:
    def __init__(self, user_id):
        self.user_id = user_id
        self.crystals = 0
        self.wordle_daily_limit = 20

    async def update(self):
        await db.users.update_one(
            {'user_id': self.user_id},
            {'$set': {'info': pickle.dumps(self)}},
            upsert=True
        )

    

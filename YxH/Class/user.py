from YxH.Database import db
import pickle
import time

class User:
  def __init__(self, user):
    self.user = user
    self.crystals = 0
    self.gems = 0
    self.coins = 0
    self.collection = {}
    self.profile_picture = None
    self.active_bot_id = 0
    self.bonus = [None, None] # [date, week]
    self.blocked = False
    self.treasure_state = False # Locked
    self.treasure = [] # [coins, gems, crystals]
    self.store = {} # {date: [id1, id2, id3]}
    self.gender = 0 # {0: None, 1: Male, -1: Female}
    self.init_time = time.time() # now

  async def update(self):
    await db.users.update_one(
      {'user_id': self.user.id},
      {'$set': {'info': pickle.dumps(self)}},
      upsert=True
    )

  def get_old(self) -> int:
    return int((time.time() - self.init_time) / 86400)

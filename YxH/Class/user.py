from YxH.Database import db
import pickle

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

  async def update(self):
    await db.users.update_one(
      {'user_id': self.user.id},
      {'$set': {'info': pickle.dumps(self)}},
      upsert=True
    )

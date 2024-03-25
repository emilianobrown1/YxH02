from YxH.Database import db
import pickle

class User:
  def __init__(user):
    self.user = user
    self.crystals = 0
    self.gems = 0
    self.coins = 0
    self.collection = {}
    self.profile_picture = None
    self.active_bot_id = 0

  async def update_crystals(self, value):
    await db.crystals.update_one(
      {'user_id': self.user.id},
      {'$set': {'crystals': value}},
      upsert=True
    )

  async def get_crystals(self):
    x = await db.crystals.find_one(
      {'user_id': user_id}
    )
    if not x:
      return 0
    return x['crystals']

  async def update_gems(self, value):
    await db.gems.update_one(
      {'user_id': self.user.id},
      {'$set': {'gems': value}},
      upsert=True
    )

  async def get_gems(self):
    x = await db.gems.find_one(
      {'user_id': user_id}
    )
    if not x:
      return 0
    return x['gems']

  async def update_coins(self, value):
    await db.coins.update_one(
      {'user_id': self.user.id},
      {'$set': {'coins': value}},
      upsert=True
    )

  async def get_coins(self):
    x = await db.coins.find_one(
      {'user_id': user_id}
    )
    if not x:
      return 0
    return x['coins']

  async def update_collection(self, value):
    await db.collection.update_one(
      {'user_id': self.user.id},
      {'$set': {'collection': pickle.dumps(value)}},
      upsert=True
    )

  async def get_collection(self):
    x = await db.collection.find_one(
      {'user_id': user_id}
    )
    if not x:
      return {}
    return pickle.loads(x['collection'])

  async def update_bot_id(self, value):
    await db.active.update_one(
      {'user_id': self.user.id},
      {'$set': {'active': value}},
      upsert=True
    )

  async def get_bot_id(self):
    x = await db.active.find_one(
      {'user_id': user_id}
    )
    if not x:
      return 0
    return x['active']

  async def update_dp(self, value):
    await db.dp.update_one(
      {'user_id': self.user.id},
      {'$set': {'dp': value}},
      upsert=True
    )

  async def get_dp(self):
    x = await db.dp.find_one(
      {'user_id': user_id}
    )
    if not x:
      return ''
    return x['dp']

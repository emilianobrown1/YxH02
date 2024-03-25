from YxH.Database import db

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

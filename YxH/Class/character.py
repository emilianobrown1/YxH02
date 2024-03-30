import pickle
import random
from YxH.Database import db

class Character:
  def __init__(self, id, image, name, category, category_name, rarity, price=0):
    self.id = id
    self.image = image
    self.name = name
    self.category = category
    self.category_name = category_name
    self.rarity = rarity
    if price == 0:
      self.price = random.choice(list(range(30000, 60001)))
    else:
      self.price = price

  async def add(self):
    await db.characters.update_one(
      {'id': self.id},
      {'$set': {'info': pickle.dumps(self)}},
      upsert=True
    )

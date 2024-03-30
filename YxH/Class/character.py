import pickle
import random
from YxH.Database import db

class AnimeCharacter:
  def __init__(self, id, image, name, anime, rarity, price=0):
    self.id = id
    self.image = image
    self.name = name
    self.anime = anime
    self.rarity = rarity
    if price == 0:
      self.price = random.choice(list(range(30000, 60001)))
    else:
      self.price = price

  async def add(self):
    await db.anime_characters.update_one(
      {'id': self.id},
      {'$set': {'info': pickle.dumps(self)}},
      upsert=True
    )
    
class YaoiYuriCharacter:
  def __init__(self, id, image, name, price=0):
    self.id = id
    self.image = image
    self.name = name
    if price == 0:
      self.price = random.choice(list(range(30000, 60001)))
    else:
      self.price = price

  async def add(self):
    await db.yaoiyuri_characters.update_one(
      {'id': self.id},
      {'$set': {'info': pickle.dumps(self)}},
      upsert=True
    )
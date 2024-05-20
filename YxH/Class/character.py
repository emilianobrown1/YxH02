import pickle
import random
from YxH.Database import db
from pyrogram.types import InlineQueryResultPhoto as iqrp
from ..Utils.templates import inline_template
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm

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
    mk = ikm([[ikb("How many I have❓", callback_data=f"howmany{id}")]])
    inline = iqrp(photo_url=self.image, thumb_url=self.image, caption=inline_template(self), reply_markup=mk)
    self.inline = inline
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
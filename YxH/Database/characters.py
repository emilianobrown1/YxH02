from . import db
import pickle
import asyncio

chars: dict = {}

async def get_all():
  global chars
  if not chars:
    x = db.anime_characters.find()
    x = await x.to_list(length=None)
    new = {}
    for y in x:
      info = pickle.loads(y["info"])
      new[info.id] = info
    chars = new
  return chars

async def get_anime_character(id):
  if id in chars:
    return chars[id]
  x = await db.anime_characters.find_one({'id': id})
  if x:
    return pickle.loads(x['info'])
  return None

async def get_anime_character_ids() -> list[int]:
  if chars:
    return list(chars)
  x = db.anime_characters.find()
  x = await x.to_list(length=None)
  return [i['id'] for i in x]

async def anime_characters_count():
  if chars:
    return len(chars)
  x = db.anime_characters.find()
  if not x:
    return 0
  return len(await x.to_list(length=None))

asyncio.create_task(get_all())

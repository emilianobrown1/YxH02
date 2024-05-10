from . import db
import pickle

async def get_anime_character(id):
  x = await db.anime_characters.find_one({'id': id})
  if x:
    return pickle.loads(x['info'])
  return None

async def get_anime_character_ids() -> list[int]:
  x = db.anime_characters.find()
  x = await x.to_list(length=None)
  return [i['id'] for i in x]

async def anime_characters_count():
  x = db.anime_characters.find()
  if not x:
    return 0
  return len(await x.to_list(length=None))

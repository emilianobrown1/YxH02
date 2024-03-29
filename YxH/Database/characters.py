from . import db
import pickle

db = db.characters

async def get_character(id):
  x = await db.find_one({'id': id})
  if x:
    return pickle.loads(x['info'])
  return None

async def characters_count():
  x = db.find()
  if not x:
    return 0
  return len(await x.to_list(length=None))

from . import db

db = db.characters

async def get_character(id):
  x = await db.find_one({'id': id})
  if x:
    return x['info']
  return {}

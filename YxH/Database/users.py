from . import db
import pickle

db = db.users

async def get_user(user_id):
  x = await db.find_one({'user_id': user_id})
  if x:
    return pickle.loads(x['info'])
  return None

async def get_all_users():
  x = db.find()
  x = await x.to_list(length=None)
  return [pickle.loads(y["info"]) for y in x]


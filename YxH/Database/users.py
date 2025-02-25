from . import db
import pickle
from .unpickler import safe_pickle_loads

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



async def get_user(user_id):
    x = await db.find_one({'user_id': user_id})
    return safe_pickle_loads(x['info']) if x else None

async def get_all_users():
    return [safe_pickle_loads(y["info"]) for y in await db.find().to_list(length=None)]

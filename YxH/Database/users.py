from . import db
import pickle
db = db.users

async def get_user(user_id):
  x = await db.find_one({'user_id': user_id})
  if x:
    return pickle.loads(x['info'])
  return None
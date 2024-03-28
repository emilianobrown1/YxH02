from . import db

db = db.bonus

# [date, week]
# Ex: [28-03-2024, 36]

async def get_bonus(user_id: int):
  x = await db.find_one({'user_id': user_id})
  if x:
    return x['bonus']
  return [None, None]

async def update_bonus(user_id: int, date, week):
  await db.update_one({'user_id': user_id}, {'$set': {'bonus': [date, week]}}, upsert=True)

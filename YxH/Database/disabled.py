from . import db

db = db.disabled

async def disable(comm: str) -> None:
  await db.insert_one({'command': comm})

async def enable(comm: str) -> None:
  await db.delete_one({'command': comm})

async def get_disabled() -> list[str]:
  x = db.find()
  x = await db.to_list(length=None)
  if not x:
    return []
  return [i['command'] for i in x]

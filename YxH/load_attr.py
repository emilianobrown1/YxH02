from .Database.users import get_user
from .Class.user import User

ex_user = User("YxH")
attr = [x for x in dir(ex_user) if not callable(x)]

async def load_attr(user_id: int):
  user = await get_user(user_id)
  for x in attr:
    if hasattr(user, x):
      continue
    setattr(user, x, getattr(ex_user, x))
  await user.update()
  return user
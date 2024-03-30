from .Database.users import get_user
from .Class.user import User

attr = [x for x in dir(User) if not callable(x)]
ex_user = User("YxH")

async def load_attr(user_id: int):
  user = await get_user(user_id)
  user_attr = [x for x in dir(user) if not callable(x)]
  for x in attr:
    if hasattr(user, x):
      continue
    setattr(user, x, getattr(ex_user, x))
  await user.update()

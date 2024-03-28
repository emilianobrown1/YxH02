from yxh import YxH

info = None

async def bot_info():
  global info
  if not info:
    info = await YxH.get_me()
  return info
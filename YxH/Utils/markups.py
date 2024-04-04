from . import ikm, ikb
from .. import bot_info
from config import SUPPORT_GROUP, SUPPORT_CHANNEL

async def start_markup():
  info = await bot_info()
  start_markup = ikm(
    [
      [
        ikb("Add me to your group", url=f"https://t.me/{info.username}?startgroup=True")
      ],
      [
        ikb("Group", url=f"https://t.me/{SUPPORT_GROUP}"),
        ikb("Channel", url=f"https://t.me/{SUPPORT_CHANNEL}")
      ]
    ]
  )
  return start_markup

def store_markup(user_id, page: int):
  dic = {1: [3, 2], 2: [1, 3], 3: [2, 1]}
  markup = ikm(
    [
      [
        ikb("<-", callback_data=f"turn|{dic[page][0]}_{user_id}"),
        ikb("Buy", callback_data=f"buy|{page}_{user_id}"),
        ikb("->", callback_data=f"turn|{dic[page][1]}_{user_id}")
      ]
    ]
  )
  return markup

def gender_markup(u):
  g = u.gender
  markup = ikm()

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
  gl = ["Other", "Haru🧍‍♂", "Yoon🧍‍♀"]
  gl[g] += " ☑️"
  return ikm(
    [
      [
        ikb(gl[1], callback_data=f"male_{u.user.id}"),
        ikb(gl[-1], callback_data=f"female_{u.user.id}")
      ],
      [
        ikb(gl[0], callback_data=f"other_{u.user.id}")
      ]
    ]
  )

def xprofile_markup(u):
  return ikm(
    [
      [
        ikb("Gender", callback_data=f"gender_{u.user.id}")
      ]
    ]
  )

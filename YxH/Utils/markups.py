from . import ikm, ikb
from .. import bot_info
from ..Class import User
from config import SUPPORT_GROUP, SUPPORT_CHANNEL
import math

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

def store_markup(user_id: int, page: int, bought: bool):
  p = '👈'
  n = '👉'
  dic = {1: [3, 2], 2: [1, 3], 3: [2, 1]}
  if not bought:
    markup = ikm(
      [
        [
          ikb(p, callback_data=f"turn|{dic[page][0]}_{user_id}"),
          ikb("Buy 💎", callback_data=f"buy|{page}_{user_id}"),
          ikb(n, callback_data=f"turn|{dic[page][1]}_{user_id}")
        ],
        [
          ikb("Close 🗑️", callback_data=f"close_{user_id}")
        ]
      ]
    )
  else:
    markup = ikm(
      [
        [
          ikb(p, callback_data=f"turn|{dic[page][0]}_{user_id}"),
          ikb(n, callback_data=f"turn|{dic[page][1]}_{user_id}")
        ],
        [
          ikb("Close 🗑️", callback_data=f"close_{user_id}")
        ]
      ]
    )
  return markup

def gender_markup(u):
  g = u.gender
  uff = u.gl
  uff[g] += " ☑️"
  return ikm(
    [
      [
        ikb(uff[1], callback_data=f"male_{u.user.id}"),
        ikb(uff[-1], callback_data=f"female_{u.user.id}")
      ],
      [
        ikb(uff[0], callback_data=f"other_{u.user.id}")
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

def acollection_markup(current: int, u: User, current_5: list[int]):
  total = math.ceil(len(u.collection)/5)
  next = current + 1
  prev = current - 1
  if next > total:
    next = 1
  if prev < 1:
    prev = total
  l = [ikb(str(i), callback_data=f'view|{current}|{i}_{u.user.id}') for i in current_5]
  res = []
  if len(current_5) > 3:
    res.append(l[:3])
    res.append(l[3:])
  else:
    res.append(l)
  res.append(
    [
      ikb('<-', callback_data=f'acoll|{current}|{prev}_{u.user.id}'),
      ikb('->', callback_data=f'acoll|{current}|{next}_{u.user.id}')
    ]
  )
  res.append(
    [
        ikb('Close', callback_data=f'close_{u.user.id}')
    ]
  )
  markup = ikm(res)
  return markup

def view_back_markup(user_id: int, current: int) -> ikm:
  return ikm(
    [
      [
        ikb('Back', callback_data=f'acoll|0|{current}_{user_id}')
      ],
      [
        ikb('Close', callback_data=f'close_{user_id}')
      ]
    ]
  )
from . import ikb, ikm
from .. import bot_info

text = "Click the button below to Register."
markup = None

async def force_start(m):
  global markup
  if not markup:
    markup = ikm(
      [
        [
          ikb("Click here", url=f"https://t.me/{(await bot_info()).username}?startgroup=True")
        ]
      ]
    )
  await m.reply(text, reply_markup=markup)

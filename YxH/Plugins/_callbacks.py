from pyrogram import Client
from ..Database.users import get_user
from ..Utils.markups import gender_markup, xprofile_markup, store_markup
from ..Utils.templates import xprofile_template, get_anime_image_and_caption
from pyrogram.types import InputMediaPhoto as imp
from ..Utils.datetime import get_date

@Client.on_callback_query()
async def cbq(_, q):
  data, actual = q.data.split("_")
  actual = int(actual)
  if actual != q.from_user.id:
    return await q.answer()
  u = await get_user(q.from_user.id)
  if data == "gender":
    await q.answer()
    await q.edit_message_reply_markup(reply_markup=gender_markup(u))
  elif data == "male":
    if u.gender != 1:
      u.gender = 1
      await q.answer()
      await q.edit_message_text(xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
  elif data == "female":
    if u.gender != -1:
      u.gender = -1
      await q.answer()
      await q.edit_message_text(xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
  elif data == "other":
    if u.gender != 0:
      u.gender = 0
      await q.answer()
      await q.edit_message_text(xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
  elif data.startswith("turn"):
    page = int(data.split("|")[1])
    date = get_date()
    chars = u.store.get(date)
    if not chars:
      await q.answer()
      return await q.message.delete()
    image, caption = await get_anime_image_and_caption(chars[page-1])
    markup = store_markup(actual, page)
    await q.answer()
    await q.edit_message_media(imp(image, caption=caption), reply_markup=markup)
from pyrogram import Client, filters
from . import YxH, get_anime_character
from ..Utils.templates import xprofile_template
from ..Utils.markups import xprofile_markup

@Client.on_message(filters.command("xprofile"))
@YxH()
async def xprof(_, m, u):
  if u.favourite_character:
    return await m.reply_photo(
      (await get_anime_character(u.favourite_character)).image,
      caption=await xprofile_template(u),
      reply_markup=xprofile_markup(u)
    )
  return await m.reply(
    await xprofile_template(u),
    reply_markup=xprofile_markup(u)
  )

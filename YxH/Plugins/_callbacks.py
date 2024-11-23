import asyncio
import math
import random

from pyrogram import Client
from pyrogram.types import CallbackQuery, InputMediaPhoto
from ..Database.users import get_user
from ..Database.characters import get_anime_character
from ..Utils.markups import (
    gender_markup,
    xprofile_markup, 
    store_markup,
    acollection_markup,
    view_back_markup
)
from ..Utils.templates import (
    xprofile_template,
    get_anime_image_and_caption,
    acollection_template
)
from pyrogram.types import InputMediaPhoto as imp
from ..Utils.datetime import get_date
from ..Class import User, AnimeCharacter
from .spinxwin import spin_cbq
from .gift import gifts_cbq
from .barracks import barracks_cbq
# MODULE FUNCTIONS IMPORTS

from .bonus import claim_cbq
from .equipments import e_cbq
from .clan import (
    settings_cbq,
    clanback_cbq,
    members_cbq,
    toggle_jr,
    toggle_v,
    join_clan,
    clan_cbq,
    leave_clan
)
from .shield import shield_cbq
from ..universal_decorator import download_image

@Client.on_callback_query()
async def cbq(_, q: CallbackQuery):
  if q.data.startswith('name'):
    id = int(q.data[4:])
    char_name = await get_anime_character(id)
    char_name = char_name.name
    return await q.answer(char_name, show_alert=True)
  elif q.data.startswith("answer"):
    return await q.answer()
  elif q.data.startswith("howmany"):
    cid = int(q.data[7:])
    u = await get_user(q.from_user.id)
    count = u.collection.get(cid, 0)
    return await q.answer(f"You have {count}.", show_alert=True)
  

  data, actual = q.data.split("_")
  actual = int(actual)
  if actual != q.from_user.id:
    return await q.answer()
  u: User = await get_user(q.from_user.id)
  if data == "gender":
    await q.answer()
    await q.edit_message_reply_markup(reply_markup=gender_markup(u))
  elif data == "male":
    if u.gender != 1:
      u.gender = 1
      await q.answer()
      await q.edit_message_text(await xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
  elif data == "female":
    if u.gender != -1:
      u.gender = -1
      await q.answer()
      await q.edit_message_text(await xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
  elif data == "other":
    if u.gender != 0:
      u.gender = 0
      await q.answer()
      await q.edit_message_text(await xprofile_template(u), reply_markup=xprofile_markup(u))
      await u.update()
    else:
      await q.answer()
      await q.edit_message_reply_markup(reply_markup=xprofile_markup(u))
  elif data == 'close':
    await q.answer()
    await q.message.delete()
  elif data.startswith("turn"):
    page = int(data.split("|")[1])
    date = get_date()
    chars = u.store.get(date)
    if not chars:
      await q.answer()
      return await q.message.delete()
    image, caption = await get_anime_image_and_caption(chars[page-1])
    markup = store_markup(actual, page, u.store_purchases[date][page - 1])
    await q.answer()
    try:
        await q.edit_message_media(imp(image, caption=caption), reply_markup=markup)
    except:
        await download_image(image, "dl.jpg")
        await q.edit_message_media(imp("dl.jpg", caption=caption), reply_markup=markup)
  elif data.startswith('buy'):
    page = int(data.split("|")[1])
    date = get_date()
    chars = u.store.get(date)
    if not chars:
      await q.answer()
      return await q.message.delete()
    char_id = u.store[date][page-1]
    char: AnimeCharacter = await get_anime_character(char_id)
    if u.gems < char.price:
      return await q.answer(f'You need {char.price-u.gems} more gems to buy this.', show_alert=True)
    await q.answer('Bought Successfully', show_alert=True)
    u.store_purchases[date][page - 1] = True
    markup = store_markup(actual, page, True)
    await q.edit_message_reply_markup(markup)
    u.gems -= char.price
    if not chars[page-1] in u.collection:
      u.collection[chars[page-1]] = 1
    else:
      u.collection[chars[page-1]] += 1
    await u.update()
  elif data.startswith('acoll'):
    current: int = int(data.split('|')[1])
    page = int(data.split('|')[2])
    if current == page:
      return await q.answer()
    coll: dict[int, int] = u.collection
    total: int = math.ceil(len(coll) / 5)
    last: int = (page * 5)
    first: int = last - 5
    char_ids: list[int] = list(coll)[first: last]
    image: str = (await get_anime_character(random.choice(char_ids))).image
    nos: list[int] = list(coll.values())[first: last]
    char_objs: list[AnimeCharacter] = await asyncio.gather(*[asyncio.create_task(get_anime_character(x)) for x in char_ids])
    char_dicts: list[dict] = [x.__dict__ for x in char_objs]
    txt: str = f"{u.user.first_name}'s collection\n"
    txt += f'page: {page}/{total}\n\n'
    txt += acollection_template(char_dicts, nos)
    markup = acollection_markup(page, u, char_ids)
    await q.answer()
    media: InputMediaPhoto = InputMediaPhoto(image, caption=txt)
    await q.edit_message_media(media, reply_markup=markup)
  elif data.startswith('view'):
    current: int = int(data.split('|')[1])
    id: int = int(data.split('|')[2])
    char_dict: dict = (await get_anime_character(id)).__dict__
    image: str = char_dict['image']
    caption: str = acollection_template([char_dict], [u.collection.get(id)])
    markup = view_back_markup(u.user.id, current)
    await q.answer()
    await q.edit_message_media(InputMediaPhoto(image, caption=caption), reply_markup=markup)
  elif data.startswith('claim'):
    await claim_cbq(_, q, u)
  elif data.startswith("treasure"):
    cry = u.crystals
    if cry < 500:
      req = 500 - cry
      return await q.answer(f"You need {req} more crystals to unlock treasure.", show_alert=True)
    u.crystals -= 500
    u.treasure_state = True
    markup = xprofile_markup(u)
    await asyncio.gather(
      q.answer("Unlocked.", show_alert=True),
      q.edit_message_reply_markup(reply_markup=markup),
      u.update()
    )
  elif data.startswith(("Axe", "Hammer", "Shovel", "Pickaxe", "Bomb")):
    await e_cbq(_, q, u)
  elif data.startswith("spin"):
    await spin_cbq(_, q, u)
  elif data.startswith("settings"):
    await settings_cbq(_, q, u)
  elif data.startswith("clanback"):
    await clanback_cbq(_, q, u)
  elif data.startswith("members"):
    await members_cbq(_, q, u)
  elif data.startswith("togglejr"):
    await toggle_jr(_, q, u)
  elif data.startswith("togglev"):
    await toggle_v(_, q, u)
  elif data.startswith("join"):
    await join_clan(_, q, u, int(data.split("_")[0].split("|")[1]))
  elif data.startswith("clan"):
    await clan_cbq(_, q, u)
  elif data.startswith("leave"):
    await leave_clan(_, q, u)    
  elif data.startswith("shield"):
    await shield_cbq(_, q, u)
  elif data.startswith("gifts"):
    await gifts_cbq(_, q, u)
  elif data.startswith("barracks"):
    await barracks_cbq(_, q, u)    
  else:
    return await q.answer("Under maintenance.", show_alert=True)

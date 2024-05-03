from pyrogram import Client, filters
from . import get_date, YxH, anime_characters_count
import random
from ..Utils.markups import store_markup
from ..Utils.templates import get_anime_image_and_caption

async def parts(user_id):
    lis = await get_user_characters(user_id)
    eve = []
    smex = []
    for x in lis:
        if len(smex) == 5:
            eve.append(smex)
            smex = []
        smex.append(x)
    if smex:
        eve.append(smex)
    return eve 

async def build_markup(lis, ids, user_id):
    x = lis
    coll = 0
    for z in lis:
        coll += len(z)
    ind = x.index(ids)
    ind += 1
    if ind == 1:
        markup = IKM([[IKB("⏩", callback_data=f"turn/{ind + 1}_{user_id}")], [IKB("5x ⏭️", callback_data=f"turn/{ind + 5}_{user_id}")], [IKB(capsify(f"Inline ({coll})"), switch_inline_query_current_chat=f"collection_{user_id}")], [IKB(capsify("close 🗑️"), callback_data=f"close_{user_id}")]])
    else:
        if x[ind-1] == x[-1]:
            markup = IKM([[IKB("⏪", callback_data=f"turn/{ind - 1}_{user_id}")], [IKB("5x ⏮️", callback_data=f"turn/{ind - 5}_{user_id}")], [IKB(capsify(f"Inline ({coll})"), switch_inline_query_current_chat=f"collection_{user_id}")], [IKB(capsify("close 🗑️"), callback_data=f"close_{user_id}")]])
        else:
            markup = IKM([[IKB("⏪", callback_data=f"turn/{ind - 1}_{user_id}"), IKB("⏩", callback_data=f"turn/{ind + 1}_{user_id}")], [IKB("5x ⏮️", callback_data=f"turn/{ind - 5}_{user_id}"), IKB("5x ⏭️", callback_data=f"turn/{ind + 5}_{user_id}")], [IKB(capsify(f"Inline ({coll})"), switch_inline_query_current_chat=f"collection_{user_id}")], [IKB(capsify("close 🗑️"), callback_data=f"close_{user_id}")]])
    return markup 

async def turn(_, q):
    page = int(q.data.split("_")[0].split("/")[1])
    ind = page - 1
    user_id = await get_switch(q.from_user.id)
    x = await parts(user_id)
    try:
        sub_lis = x[ind]
    except:
        return await q.answer()
    await q.answer(capsify("turning to page") + " " + str(page))
    markup = await build_markup(x, sub_lis, user_id)
    z = await get_user_characters(user_id)
    txt = await _.first_name(user_id) + "'s" + " " + capsify("collection")
    txt += "\n"
    pgg = len(z) / 5
    if isinstance(pgg, int):
        omfoo = pgg
    else:
        omfoo = int(pgg) + 1
    txt += f"{capsify('page')} {page}/{omfoo}"
    txt += "\n\n"
    for y in sub_lis:
        char_info = await get_character(int(y))
        owned = z[y]
        txt += f"♦️ {char_info['name']} (x{owned})\n  [{char_info['anime']}]\n  🆔 : {y}"
        txt += "\n\n"
    await q.edit_message_text(txt, reply_markup=markup)

@Client.on_message(filters.command("collection"))
@YxH(private=False)
async def coll(_, m, user_id):
    user_id = await
    x = await parts(user_id)
    if not x:
        return await m.reply(capsify("your collection is empty !"))
    sub_lis = x[0]
    markup = await build_markup(x, sub_lis, user_id)
    z = await get_user_characters(user_id)
    txt = await _.first_name(user_id) + "'s" + " " + capsify("collection")
    txt += "\n"
    pgg = len(z) / 5
    if isinstance(pgg, int):
        omfoo = pgg
    else:
        omfoo = int(pgg) + 1
    txt += f"{capsify('page')} 1/{omfoo}"
    txt += "\n\n"
    for y in sub_lis:
        char_info = await get_character(int(y))
        owned = z[y]
        txt += f"♦️ {char_info['name']} (x{owned})\n  [{char_info['anime']}]\n  🆔 : {y}"
        txt += "\n\n"
    await m.reply(txt, reply_markup=markup)
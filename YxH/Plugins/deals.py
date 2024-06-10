from pyrogram import Client, filters
from ..universal_decorator import YxH
from ..Database.users import get_user
from ..Database.characters import get_anime_character
import asyncio
from yxh import YxH as app
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb

deals_dic = {} # {seller: {ID: buyer}}

@Client.on_message(filters.command('deal'))
@YxH(private=False)
async def deal(_, m, u):
    try:
        char_id = int(m.text.split()[1])
        price = int(m.text.split()[2])
    except:
        return await m.reply('**Usage:** `/deal [character] [price]`')
    if not char_id in u.collection:
        return await m.reply('**You don\'t own this character.**')
    if char_id in u.deals:
        return await m.reply('**This character is already in your deals list.**')
    if len(u.deals) == 5:
        return await m.reply('**Deals slot is Full.**')
    u.deals[char_id] = price
    if u.collection[char_id] == 1:
        u.collection.pop(char_id)
    else:
        u.collection[char_id] -= 1
    await m.reply(f'Character of ID `{char_id}` has been added to your deals for `{price}` Gems.')
    await u.update()
    
def deals_markup(ids: list[int]) -> ikm:
    txt = "|".join(ids)
    return ikm([[ikb("View Inline", switch_inline_query_current_chat=f"view|{txt}")]])

@Client.on_message(filters.command('deals'))
@YxH(private=False)
async def deals(_, m, u):
    try:
        if m.reply_to_message:
            t_id = m.reply_to_message.from_user.id
        else:
            t_id = int(m.text.split()[1])
    except:
        return await m.reply('**Either reply to an user or provide their ID.**')
    t_u = await get_user(t_id)
    if not t_u:
        return await m.reply('**User Not Found.**')
    if not t_u.deals:
        return await m.reply(f'**{t_u.user.first_name}** Has no deals currently.')
    txt = f'**{t_u.user.first_name}**\'s Deals\n\n'
    for x, y in enumerate(t_u.deals):
        char = await get_anime_character(y)
        txt += f'`{x+1}.` {char.name} ({char.id}): `{t_u.deals[y]}` Gems\n'
    txt += '\n'
    txt += f'For purchasing, use `/buy {t_id}` [character]'
    return await m.reply(txt, reply_markup=deals_markup(list(t_u.deals)))

@Client.on_message(filters.command('buy'))
@YxH(private=False)
async def buy(_, m, u):
    try:
        t_id = int(m.text.split()[1])
        char_id = int(m.text.split()[2])
    except:
        return await m.reply('**Usage:** `/buy [user id] [character]`')
    t_u = await get_user(t_id)
    if not t_u:
        return await m.reply('**User Not Found.**')
    if not char_id in t_u.deals:
        return await m.reply('**Character not found in user deals.**')
    if u.gems < t_u.deals[char_id]:
        return await m.reply(f'You need `{t_u.deals[char_id]-u.gems}` more gem(s) to buy.')
    deals_dic[t_id] = deals_dic.get(t_id, {})
    deals_dic[t_id][char_id] = u.user.id
    price = t_u.deals[char_id]
    u.gems -= price
    t_u.gems += price
    t_u.deals.pop(char_id)
    await u.update()
    await t_u.update()
    await _.send_message(t_id, f'Character of ID `{char_id}` has been bought for `{price}` Gems.')
    await m.reply('**Your Deal Has Been Queued.**')

async def task():
    while True:
        to_rem = {}
        for x in deals_dic:
            for char in x:
                user_id = x[char]
                user = await get_user(user_id)
                user.collection[char] += user.collection.get(char, 0) + 1
                await user.update()
                await app.send_message(user_id, f'Character of ID `{char}` has been added to your collection.')
                to_rem[x] = to_rem.get(x, []) + [char]
        for x in to_rem:
            for y in x:
                del deals_dic[x][y]
        await asyncio.sleep(1)

asyncio.create_task(task())
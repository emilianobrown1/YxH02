from pyrogram import Client, filters
from ..universal_decorator import YxH
from ..Database.users import get_user, get_all_users
from ..Database.characters import get_anime_character
import asyncio
from yxh import YxH as app
from pyrogram.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
import random

deals_dic = {} # {seller: {ID: buyer}}

@Client.on_message(filters.command('deal'))
@YxH(private=False, min_old=3)
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
    if price < 10000 or price > 200000:
        return await m.reply('Deal price should be in between `10000` and `200000`.')
    u.deals[char_id] = price
    if u.collection[char_id] == 1:
        u.collection.pop(char_id)
    else:
        u.collection[char_id] -= 1
    await m.reply(f'Character of ID `{char_id}` has been added to your deals for `{price}` Gems.')
    await u.update()
    
def deals_markup(ids: list[int]) -> ikm:
    txt = "|".join(list(map(str, ids)))
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
        #return await m.reply('**Either reply to an user or provide their ID.**')
        some = [user for user in await get_all_users() if user.deals]
        if not some or (len(some) == 1 and some[0].user.id == u.user.id):
            return await m.reply("**No Dealers Available Right Now.**")
        t_id = m.from_user.id
        while t_id == m.from_user.id:
            t_id = random.choice(some).user.id
    if t_id == m.from_user.id:
        return
    t_u = await get_user(t_id)
    if not t_u:
        return await m.reply('**User Not Found.**')
    if not t_u.deals:
        return await m.reply(f'**{t_u.user.first_name}** Has no deals currently.')
    txt = f'**{t_u.user.first_name}**\'s Deals\n\n'
    for y in t_u.deals:
        char = await get_anime_character(y)
        have = u.collection.get(y, 0)
        col = "🔴" if have == 0 else "🟢"
        txt += f'{col} {char.name} (`{char.id}`)\nPrice: `{t_u.deals[y]}` Gems\nYou have `{have}`.\n'
    txt += '\n'
    txt += f'For purchasing, use `/buy {t_id} `[character_id]'
    return await m.reply(txt, reply_markup=deals_markup(list(t_u.deals)))

@Client.on_message(filters.command("rdeal"))
@YxH()
async def rdeal(_, m, u):
    try:
        id = int(m.text.split()[1])
    except:
        return await m.reply("**Usage:** `/rdeal [character]`")
    if not id in u.deals:
        return await m.reply("**This Character is not in your deals.**")
    u.deals.pop(id)
    u.collection[id] = u.collection.get(id, 0) + 1
    await m.reply(f"Character of ID `{id}` has been removed from your deals.")
    await u.update()

@Client.on_message(filters.command('mydeals'))
@YxH()
async def mydeals(_, m, u):
    if not u.deals:
        return await m.reply(f'You having no active deals currently.')
    txt = f'**{u.user.first_name}**\'s Deals\n\n'
    for x, y in enumerate(u.deals):
        char = await get_anime_character(y)
        txt += f'`{x+1}.` {char.name} ({char.id}): `{u.deals[y]}` Gems\n'
    txt += '\n'
    txt += f'For removing, use `/rdeal [character]`'
    return await m.reply(txt, reply_markup=deals_markup(list(u.deals)))

@Client.on_message(filters.command('buy'))
@YxH(private=False)
async def buy(_, m, u):
    try:
        t_id = int(m.text.split()[1])
        char_id = int(m.text.split()[2])
    except:
        return await m.reply('**Usage:** `/buy [user_id] [character_id]`')
    if t_id == m.from_user.id:
        return
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
            for char in deals_dic[x]:
                user_id = deals_dic[x][char]
                user = await get_user(user_id)
                user.collection[char] = user.collection.get(char, 0) + 1
                await user.update()
                await app.send_message(user_id, f'Character of ID `{char}` has been added to your collection.')
                to_rem[x] = to_rem.get(x, []) + [char]
        for x in to_rem:
            for y in to_rem[x]:
                del deals_dic[x][y]
        await asyncio.sleep(1)

asyncio.create_task(task())
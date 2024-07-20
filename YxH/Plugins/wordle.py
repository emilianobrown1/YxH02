from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from . import get_date, YxH
from ..Class import user
from ..Class.wordle import wordle
from ..Database.wordle import add_game, get_wordle_dic, get_avg, incr_game, get_today_games, get_all_games, add_crystal
from ..Database.users import get_user
from .wordle_image import make_secured_image
from easy_words import words
import random
import re
import time
import asyncio
from bs4 import BeautifulSoup
import requests
import string

asc = string.ascii_letters
dic = {}
time_out_dic = {}

def _get_soup_object(url, parser="html.parser"):
    return BeautifulSoup(requests.get(url).text, parser)

def is_valid(text: str) -> bool:
    term: str = text
    try:
        html = _get_soup_object(f"http://wordnetweb.princeton.edu/perl/webwn?s={term}")
        types = html.findAll("h3")
        lists = html.findAll("ul")
        for a in types:
            reg = str(lists[types.index(a)])
            if any(len(x) > 5 or ' ' in str(x) for x in re.findall(r'\((.*?)\)', reg)):
                return True
        return False
    except:
        return False

def get_reward(correct_guess: bool) -> int:
    return 1 if correct_guess else 0

def update_negated(word, text, lis):
    for i in text:
        if i not in word and i.upper() not in lis:
            lis.append(i.upper())
    return lis

@Client.on_message(filters.command("wordle"))
@YxH(private=False)
async def wordle_command(client, message, user):
    global dic
    user_id = message.from_user.id
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Terminate", callback_data=f'terminate_{user_id}')],
        [InlineKeyboardButton("Close", callback_data=f'close_{user_id}')]
    ])
    if user_id in dic:
        return await message.reply('You are already in a game, wanna terminate it?', reply_markup=markup)

    word = random.choice(words)
    dic[user_id] = [word, [], [], time.time()]
    txt = f'{message.from_user.mention}, Wordle has been started, guess the 5-letter word within 6 chances!\n\nEnter your first word!'
    await message.reply(txt, reply_markup=markup)

@Client.on_message(filters.command("cwordle"))
async def cwordle(client, message):
    global dic, time_out_dic
    user_id = message.from_user.id
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Terminate", callback_data=f'terminate_{user_id}')],
        [InlineKeyboardButton("Close", callback_data=f'close_{user_id}')]
    ])
    if user_id in dic:
        return await message.reply('You are already in a game, wanna terminate it?', reply_markup=markup)

    word = random.choice(words)
    dic[user_id] = [word, [], [], time.time()]
    time_out_dic[user_id] = [message.chat.id, time.time()]
    txt = f'{message.from_user.mention}, Challenge Wordle has been started, guess the 5-letter word within 6 chances!\n\nEnter your first word!'
    await message.reply(txt, reply_markup=markup)

@Client.on_message(filters.group)
async def cwf(client, message):
    global dic, time_out_dic
    user_id = message.from_user.id
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Start Again", callback_data=f'startwordle_{user_id}')],
        [InlineKeyboardButton("Close", callback_data=f'close_{user_id}')]
    ])
    if user_id not in dic or not message.text or len(message.text.split()) != 1 or len(message.text) != 5 or any(g not in asc for g in message.text):
        return

    word = dic[user_id][0]
    lis = dic[user_id][1]
    neg = dic[user_id][2]

    if message.text.lower() in lis:
        return await message.reply('Word has been entered already!')

    if not is_valid(message.text.lower()):
        return await message.reply('Invalid English word!')

    if user_id in time_out_dic:
        time_out_dic[user_id] = [message.chat.id, time.time()]

    update_negated(word, message.text, neg)
    cap = f'Time taken: {int(time.time() - dic[user_id][3])} seconds'
    if message.text.lower() == word:
        com_len = len(lis) + 1
        dic.pop(user_id)
        await add_game(user_id)
        gg = await get_today_games(user_id)
        if gg < 20:
            rew = get_reward(True)
            await add_crystal(user_id, rew)
            await incr_game(user_id)
            await add_crystal(user_id, com_len)
            await user.update()
            return await message.reply(f'Guessed word in {com_len} attempts! You got {rew} crystal as reward. {cap}!', reply_markup=markup)
        else:
            await incr_game(user_id)
            await add_crystal(user_id, com_len)
            return await message.reply(f'Guessed word in {com_len} attempts! You got no tokens as daily limit reached. {cap}!', reply_markup=markup)

    lis.append(message.text.lower())
    dic[user_id][2] = neg
    new = ', '.join(f'`{li}`' for li in lis)
    old = ', '.join(f'__{ne}__' for ne in neg)

    # Create and send image with the current game state
    image_path = await make_secured_image(user_id, word, lis)
    await client.send_photo(message.chat.id, photo=image_path, caption=f'Guess {len(lis)} / 6\n\nNegated: {old}\n\nUsed: {new}', reply_markup=markup)

    if len(lis) > 5:
        dic.pop(user_id)
        if user_id in time_out_dic:
            time_out_dic.pop(user_id)
        return await message.reply(f"Out of attempts, the word is '{word}', better luck next time!", reply_markup=markup)

@Client.on_callback_query(filters.regex(r'^terminate_'))
async def terminate(client, query):
    global dic, time_out_dic
    user_id = int(query.data.split('_')[1])
    if user_id not in dic:
        return await query.answer("You are not in a game!", show_alert=True)
    await query.answer('Terminating...')
    dic.pop(user_id)
    if user_id in time_out_dic:
        time_out_dic.pop(user_id)
    await query.edit_message_text("Game terminated!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Start Again", callback_data=f'startwordle_{user_id}')]]))

@Client.on_callback_query(filters.regex(r'^startwordle_'))
async def start_again(client, query):
    global dic
    user_id = int(query.data.split('_')[1])
    if user_id in dic:
        return await query.answer("You are already in a game!", show_alert=True)
    await query.answer('Starting...')
    word = random.choice(words)
    dic[user_id] = [word, [], [], time.time()]
    txt = f'{(await client.get_users(user_id)).mention}, Wordle has been started, guess the 5-letter word within 6 chances!\n\nEnter your first word!'
    await client.send_message(query.message.chat.id, txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Terminate", callback_data=f'terminate_{user_id}')]]))

@Client.on_message(filters.command("wtop"))
async def wtop(client, message):
    dic = await get_wordle_dic()
    if not dic:
        return await message.reply("Wordle leaderboard empty!")
    ok = await message.reply("Getting Wordle leaderboard...")
    nset = {y: int(dic[y]) for y in dic}
    dic = sorted(nset.items(), key=lambda x: x[1], reverse=True)
    txt = "Wordle Leaderboard\n\n"
    a = 1
    for i in dic:
        avg = await get_avg(int(i[0]))
        txt += f'{a}. {(await client.get_users(int(i[0]))).mention} :- {i[1]} ({str(avg)[:4] if len(str(avg)) > 4 else str(avg)})\n'
        a += 1
        if a > 10:
            break
    await ok.edit(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data=f'close_{message.from_user.id}')]]))

async def time_out_func():
    global time_out_dic, dic
    while True:
        to_pop = []
        for x in time_out_dic:
            if time.time() - time_out_dic[x][1] > 300:  # 5 minutes timeout
                to_pop.append(x)

        for user_id in to_pop:
            chat_id = time_out_dic[user_id][0]
            await Client.send_message(chat_id, f"Challenge Wordle game for user {user_id} has timed out!")
            time_out_dic.pop(user_id)
            if user_id in dic:
                dic.pop(user_id)

        await asyncio.sleep(60)

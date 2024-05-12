from . import get_chat, get_user
from ..Class import Chat
from .image_maker import make_image
from .watchers import fw_watcher
# import random
import asyncio

count: dict[int, int] = {}

async def cwf(_, m):
    global count
    try:
        chat_id = m.chat.id
        user_id = m.from_user.id
    except:
        return
    chat: Chat = await get_chat(chat_id)
    user = await get_user(user_id)
    if user.blocked:
        return
    if chat.fw_status:
        if m.text:
            if m.text.lower() == chat.fw_status:
                await m.reply('Congrats kiddo.')
                chat.fw_status = None
                if user_id in chat.words:
                    chat.words[user_id] += 1
                else:
                    chat.words[user_id] = 1
                if chat_id in user.words:
                    user.words[chat_id] += 1
                else:
                    user.words[chat_id] = 1
                await asyncio.gather(
                    user.update(),
                    chat.update()
                )
    if chat_id in count:
        count[chat_id] += 1
    else:
        count[chat_id] = 1
    if count[chat_id] == chat.fw_cooldown:
        count[chat_id] = 0
        word = 'Example'
        chat.fw_status = word.lower()
        await chat.update()
        im = make_image(word, '@alpha')
        await _.send_photo(chat_id, im, caption='Complete')

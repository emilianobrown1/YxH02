from .. import bot_info
from ..Utils.datetime import get_date, get_week
from ..Utils.snake import snake_manager, create_snake_board
from ..Database.users import get_user
from ..Database.chats import get_chat
from ..Database.characters import get_anime_character, anime_characters_count
from ..universal_decorator import YxH
from pyrogram.types import (
    InlineKeyboardMarkup as ikm,
    InlineKeyboardButton as ikb
)

def grt(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

__all__ = ['snake_manager', 'create_snake_board']
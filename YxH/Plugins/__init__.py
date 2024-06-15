from .. import bot_info
from ..Utils.datetime import get_date, get_week
from ..Database.users import get_user
from ..Database.chats import get_chat
from ..Database.characters import get_anime_character, anime_characters_count
from ..universal_decorator import YxH
import requests
from PIL import Image
from io import BytesIO

def download_image(url, id) -> str:
    x = requests.get(url).content
    im = Image.open(BytesIO(x))
    path = f"Characters/{im}.jpg"
    im.save(path)
    return path
    
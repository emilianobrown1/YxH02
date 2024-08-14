from pyrogram import Client, filters
from ..Class.user import User
from ..Utils.strings import start_text
from ..Utils.markups import start_markup
from ..Database.users import get_user
from ..Database.clan import get_clan
from .clan import clan_info

@Client.on_message(filters.command("start") & filters.private)
async def start(_, m):
    if "clan_" in m.text:
        clan_id = int(m.text.split("_")[1])
        clan_data = await get_clan(clan_id)
        txt, markup = await clan_info(clan_data, m.from_user.id)
        return await m.reply(txt, reply_markup=markup)

    # Send welcome photo and message
    await m.reply_photo("Images/start.JPG", start_text.format(m.from_user.first_name), reply_markup=await start_markup())

    user = await get_user(m.from_user.id)

    if not user:
        # Create a new user
        u = User(m.from_user.id)
        await u.update()

       
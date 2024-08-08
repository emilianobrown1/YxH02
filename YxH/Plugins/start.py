from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from ..Class import User
from ..Utils.strings import start_text
from ..Utils.markups import start_markup
from ..Database.users import get_user
from ..Database.clan import get_clan
from .clan import clan_info

@Client.on_message(filters.command("start") & filters.private)
async def start(_, m):
  if "clan_" in m.text:
      txt, markup = await clan_info(await get_clan(int(m.text.split("_")[1])), m.from_user.id)
      return await m.reply(txt, reply_markup=markup)
  await m.reply_photo("Images/start.JPG", start_text.format(m.from_user.first_name), reply_markup=await start_markup())
  user = await get_user(m.from_user.id)
  if not user:
    # Create new user
    u = User(m.from_user)
    await u.update()

    # Award 100 crystals to the new user
    u.crystals += 100
    await u.update()  # Save the updated user data to the database
else:
    # Handle rewards for users who have been invited
    if user.invited_by:
        inviter = await get_user(user.invited_by)
        if inviter:
            inviter.crystals += 50
            await inviter.update()
            user.invited_by = None  # Reset after rewarding
            await user.update()

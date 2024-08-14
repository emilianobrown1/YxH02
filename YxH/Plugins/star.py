from pyrogram import Client, filters
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

    # Send welcome photo and message
    await m.reply_photo("Images/start.JPG", start_text.format(m.from_user.first_name), reply_markup=await start_markup())

    user = await get_user(m.from_user.id)

    if not user:
        # Create new user
        u = User(m.from_user)
        u.crystals += 50  # Add 50 crystals to the new user

        # Check if the user was invited via an invite link
        if len(m.command) > 1:
            inviter_id = int(m.command[1])  # Get inviter ID from the start command
            inviter = await get_user(inviter_id)
            if inviter:
                u.invited_by = inviter_id  # Set the inviter ID for the new user
                inviter.crystals += 20  # Add 20 crystals to the inviter
                await inviter.update()  # Update the inviter's data in the database

        await u.update()  # Update the new user's data in the database

        # Notify the new user and optionally the inviter
        await m.reply("Welcome! You've received 50 crystals as a new user!")
        if u.invited_by:
            await m.reply("Your inviter has been rewarded with 20 crystals!")

    else:
        # If the user already exists, do nothing or send a welcome back message
        await m.reply("Welcome back!")


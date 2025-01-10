from pyrogram import Client, filters
from ..Class.user import User
from ..Utils.strings import start_text
from ..Utils.markups import start_markup
from ..Database.users import get_user
from ..Database.clan import get_clan
from .clan import clan_info
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    try:
        # Check for clan related start command
        if "clan_" in message.text:
            clan_id = int(message.text.split("_")[1])
            clan_data = await get_clan(clan_id)
            txt, markup = await clan_info(clan_data, message.from_user.id)
            return await message.reply(txt, reply_markup=markup)

        # Respond with a welcome image and message
        await message.reply_photo("Images/start.JPG", start_text.format(message.from_user.first_name), reply_markup=await start_markup())

        user = await get_user(message.from_user.id)

        if user is None:
            # Create a new user and assign initial crystals
            new_user = User(message.from_user.id)
            new_user.crystals += 50  # Add initial 50 crystals

            # Handle user invite mechanism if present in the command
            if len(message.command) > 1:
                try:
                    inviter_id = int(message.command[1])
                    inviter = await get_user(inviter_id)
                    if inviter:
                        new_user.invited_by = inviter_id
                        inviter.crystals += 20  # Reward inviter with 20 crystals
                        await inviter.update()
                        logger.info(f"Inviter {inviter_id} rewarded with 20 crystals.")
                except ValueError:
                    logger.warning("Invalid invite ID provided.")
                    pass  # No action on invalid invite ID

            # Save the new user in the database
            await new_user.update()
            await message.reply("Welcome! You have received 50 crystals as a new user!")
            if new_user.invited_by:
                await message.reply("Your inviter has been rewarded with 20 crystals!")
            logger.info(f"New user {new_user.id} created and updated.")
        else:
            # Welcome the existing user
            await message.reply("Welcome back! Glad to see you again!")
            logger.info(f"Existing user {user.id} logged in.")

    except Exception as error:
        logger.error(f"Error occurred during the /start command: {error}")
        await message.reply("An error occurred while processing your request. Please try again later.")

from pyrogram import Client, filters
from . import YxH

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
            new_user = User(message.from_user)
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


@Client.on_message(filters.command("barracks"))
@YxH()
async def barracks(_, m, u):
    # Parse the count from the command
    spl = m.text.split()
    if len(spl) < 2:
        return await m.reply(
            f"💡 **Usage:** `/barracks 1`\n\n"
            f"🏰 **Your Current Barracks:** `{u.barracks if hasattr(u, 'barracks') else 0}`\n"
            f"💎 **Each Barrack Costs:** `100 Crystals`\n"
            f"🔢 **Purchase Limit:** `1 Barrack at a time`"
        )

    try:
        count = int(spl[1])  # Get the count
    except ValueError:
        return await m.reply("Please provide a valid number of barracks to purchase.")

    # Only allow purchasing 1 barrack at a time
    if count != 1:
        return await m.reply(
            f"❌ **You can only buy 1 barrack at a time!**\n\n"
            f"💡 **Usage:** `/barracks 1`"
        )

    # Cost for 1 barrack
    cost = 100

    # Ensure the `barracks` attribute exists
    if not hasattr(u, "barracks"):
        u.barracks = 0  # Initialize if not present

    # Check if the user has enough crystals
    if u.crystals < cost:
        return await m.reply(
            f"❌ **Not enough Crystals!**\n\n"
            f"You need `{cost - u.crystals}` more crystals to buy 1 barrack.\n"
            f"💎 **Your Crystals:** `{u.crystals}`\n"
            f"🏰 **Your Current Barracks:** `{u.barracks}`"
        )

    # Deduct crystals and increment barracks count
    u.crystals -= cost
    u.barracks += 1  # Safely increment the barrack count

    # Update the user in the database
    await u.update()

    # Send confirmation with an image
    caption = (
        f"🎉 **Congratulations, Commander!**\n\n"
        f"🏰 You successfully built `1` barrack 🛡️ to train your troops!\n\n"
        f"💎 **Crystals Spent:** `100`\n"
        f"🏰 **Total Barracks Now:** `{u.barracks}`\n"
        f"💪 **Prepare Your Army and Lead to Glory!**"
    )
    await m.reply_photo(
        "Images/barrack.jpg",  # Replace with the actual image path or URL
        caption=caption
    )
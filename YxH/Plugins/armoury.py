from pyrogram import Client, filters
from . import YxH
from ..Database.users import get_user
from ..Class.user import User  # Import your User class


@Client.on_message(filters.command("armoury"))
async def display_armoury(client, message):
    user_id = message.from_user.id

    # Fetch user data (Replace with your actual database fetching logic)
    user = await get_user_data(user_id)

    # Create the Armoury display
    response = "Your Armoury\n\n"

    # Trops section
    response += "**Trops**:\n"
    for trop, count in user.armoury["Trops"].items():
        response += f"{trop} = {count}\n"

    # Powers section
    response += "\nPowers:\n"
    for power, count in user.armoury["Powers"].items():
        response += f"{power} = {count}\n"

    # Beasts section
    response += "\nBeasts:\n"
    for beast, count in user.armoury["Beasts"].items():
        response += f"{beast} = {count}\n"

    # Send the response
    await message.reply_text(response)

async def get_user_data(user_id):
    # Replace this with your logic to fetch the user instance from the database
    user = User(user_id)
    # Simulate loading data from a database
    await user.update()
    return user


from pyrogram import Client, filters
from . import YxH
from ..Class.user import User  # Import your User class


@Client.on_message(filters.command("armoury"))
@YxH()
async def display_armoury(_, m, u: User):
    # Create the Armoury display
    response = "Your Armoury\n\n"

    # Trops section
    response += "**Trops**:\n"
    for trop, count in u.armoury.get("Trops", {}).items():
        response += f"{trop} = {count}\n"

    # Powers section
    response += "\nPowers:\n"
    for power, count in u.armoury.get("Powers", {}).items():
        response += f"{power} = {count}\n"

    # Beasts section
    response += "\nBeasts:\n"
    for beast, count in u.armoury.get("Beasts", {}).items():
        response += f"{beast} = {count}\n"

    # Send the response
    await m.reply_text(response)

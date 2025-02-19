from pyrogram import Client, filters
from ..Class.user import User
from . import YxH
import time 

# Beast names categorized
PROTECTORS = {
    "Titanus Aegisorn": "Titanus Aegisorn",
    "Glacelynx": "Glacelynx",
    "Voltiscar": "Voltiscar",
    "Cerberus": "Cerberus"
}

ATTACKERS = {
    "Ignirax": "Ignirax",
    "Frostclaw": "Frostclaw",
    "Vilescale": "Vilescale",
    "Pyraxion": "Pyraxion"
}

POWERS = {
    "Darkness Shadow": "Darkness Shadow",
    "Frost Snow": "Frost Snow",
    "Thunder Storm": "Thunder Storm",
    "Nature Ground": "Nature Ground",
    "Flame Heat Inferno": "Flame Heat Inferno",
    "Aqua Jet": "Aqua Jet"
}

@Client.on_message(filters.command("barracks"))
@YxH()
async def barracks(_, m, u):
    spl = m.text.split()
    if len(spl) < 2:
        return await m.reply(
            f"💡 **Usage:** `/barracks 1`\n\n"
            f"🏰 **Your Current Barracks:** `{len(u.barracks)}`\n"
            f"💎 **Each Barrack Costs:** `100 Crystals`\n"
            f"🔢 **Purchase Limit:** `1 Barrack at a time`"
        )

    try:
        count = int(spl[1])
    except ValueError:
        return await m.reply("❌ Please provide a valid number of barracks to purchase.")

    if count != 1:
        return await m.reply("❌ You can only buy 1 barrack at a time!")

    cost = 100
    if u.crystals < cost:
        return await m.reply(
            f"❌ Not enough Crystals!\n\n"
            f"You need `{cost - u.crystals}` more crystals to buy 1 barrack.\n"
            f"💎 **Your Crystals:** `{u.crystals}`\n"
            f"🏰 **Your Current Barracks:** `{len(u.barracks)}`"
        )

    # Deduct crystals and add a new barrack (store timestamp)
    u.crystals -= cost
    u.barracks.append(time.time())

    await u.update()

    await m.reply_photo(
        "Images/barrack.jpg",  # Ensure the file exists or use a URL
        caption=(
            f"🎉 **Congratulations, Commander!**\n\n"
            f"🏰 You successfully built `1` barrack 🛡️ to train your troops!\n\n"
            f"💎 **Crystals Spent:** `100`\n"
            f"🏰 **Total Barracks Now:** `{len(u.barracks)}`\n"
            f"💪 **Prepare Your Army and Lead to Glory!**"
        )
    )



@Client.on_message(filters.command("my_barracks"))
@YxH()
async def my_barracks(_, m, u):
    if not u.barracks:
        return await m.reply("🏰 You haven't built any barracks yet! Use `/barracks 1` to get started.")

    # Formatting troops, powers, and beasts count
    troops_text = "\n".join([f"🔹 **{k.capitalize()}:** `{v}`" for k, v in u.troops.items()])
    powers_text = "\n".join([f"⚡ **{v}:** `{u.powers.get(k, 0)}`" for k, v in POWERS.items()])
    
    # Categorizing beasts into Protectors and Attackers
    protectors_text = "\n".join([f"🛡 **{v}:** `{u.beasts.get(k, 0)}`" for k, v in PROTECTORS.items()])
    attackers_text = "\n".join([f"⚔ **{v}:** `{u.beasts.get(k, 0)}`" for k, v in ATTACKERS.items()])

    # Creating the final message
    message = (
        f"🏰 **Your Barracks Overview:**\n"
        f"📦 **Total Barracks:** `{len(u.barracks)}`\n\n"
        f"👥 **Troops:**\n{troops_text if troops_text else 'None'}\n\n"
        f"⚡ **Powers:**\n{powers_text if powers_text else 'None'}\n\n"
        f"🐉 **Beasts:**\n\n"
        f"🛡 **PROTECTORS**\n{protectors_text if protectors_text else 'None'}\n\n"
        f"⚔ **ATTACKERS**\n{attackers_text if attackers_text else 'None'}"
    )

    await m.reply_photo(
        "Images/barrack.jpg",  # Using the same image as the barracks command
        caption=message
    )

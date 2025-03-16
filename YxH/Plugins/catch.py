from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from . import YxH, get_user, get_chat
from ..Class.user import User
import random
import asyncio

beast_count: dict[int, int] = {}

BEAST_INFO = {
    "Titanus Aegisorn": {
        "Role": "Shield Protector",
        "Powers": ["Aqua Jet", "Natural Ground"],
        "Weakness": "Flame Heat Inferno",
        "Image": "Beast/Titanus.jpg"
    },
    "Voltaryn": {
        "Role": "Collection Protector",
        "Powers": ["Thunder Storm", "Darkness Shadow"],
        "Weakness": "Natural Ground",
        "Image": "Beast/Voltiscar.jpg"
    },
    "Cerberus": {
        "Role": "Treasure Protector",
        "Powers": ["Flame Heat Inferno", "Darkness Shadow"],
        "Weakness": "None specified",
        "Image": "Beast/Cerberus.jpg"
    },
    "Vilescale": {
        "Role": "Collection Attacker",
        "Powers": ["Venom", "Natural Ground"],
        "Weakness": "Lightning, Darkness Shadow",
        "Image": "Beast/Vilescale.jpg"
    },
    "Frostclaw": {
        "Role": "Crystal Attacker",
        "Powers": ["Strength", "Frost Snow"],
        "Weakness": "Speed, Thunder Storm, Darkness Shadow",
        "Image": "Beast/Frostclaw.jpg"
    },
    "Pyraxion": {
        "Role": "Treasury Attacker",
        "Powers": ["Darkness Shadow", "Flame Heat Inferno"],
        "Weakness": "Speed, Natural Ground",
        "Image": "Beast/Phoenix.jpg"
    },
    "Glacelynx": {
        "Role": "Crystal Protector",
        "Powers": ["Frost Snow", "Thunder Storm", "Speed"],
        "Weakness": "Strength",
        "Image": "Beast/Glacelynx.jpg"
    },
    "Ignirax": {
        "Role": "Shield Attacker",
        "Powers": ["Fire", "Natural Ground"],
        "Weakness": "Aqua Jet, Strength",
        "Image": "Beast/Ignirax.jpg"
    }
}

async def beast_spawner(_, m):
    global beast_count
    try:
        user_id = m.from_user.id
        chat_id = m.chat.id
        user, chat = await asyncio.gather(
            get_user(user_id),
            get_chat(chat_id)
        )
    except:
        return

    if not user or user.blocked:
        return

    cooldown = 250  # Fixed cooldown of 250 messages

    
    # Increment message count for the chat
    beast_count[chat_id] = beast_count.get(chat_id, 0) + 1

    if beast_count[chat_id] >= cooldown:
        selected_beast = random.choice(list(BEAST_INFO.keys()))
        beast_data = BEAST_INFO[selected_beast]
        code = random.randint(2000, 5000)
        cost = random.randint(35, 100)

        chat.beast_status = {
            'role': beast_data['Role'],
            'code': code,
            'name': selected_beast,
            'cost': cost,
            'image': beast_data['Image']
        }
        await chat.update()  # Save updated chat data

        caption = (
            f"🦖 A Wild Beast Appeared! 🦖\n\n"
            f"**name:** selected_beast\n"
            f"**Cost:** {cost} Crystals\n\n"
            "Use `/catch [code]` to capture it!"
        )
        markup = ikm([[ikb("✨ Catch Beast ✨", callback_data=f"catch_{code}")]])

        await _.send_photo(
            chat_id,
            beast_data['Image'],
            caption=caption,
            reply_markup=markup
        )

        beast_count[chat_id] = 0  # Reset the count after spawning


@Client.on_message(filters.command("catch"))
@YxH(private=False)
async def catch_command(_, m, u):
    chat = await get_chat(m.chat.id)
    if not chat.beast_status:
        return await m.reply("No beast to catch here! 🏜")

    args = m.text.split()
    if len(args) < 2:
        return await m.reply("❌ Please provide the beast's code. Example: `/catch 1234`")

    try:
        provided_code = int(args[1])
    except ValueError:
        return await m.reply("❌ Invalid code. Must be a number.")

    if provided_code != chat.beast_status['code']:
        return await m.reply("❌ Incorrect code! Try again.")

    cost = chat.beast_status['cost']
    if u.crystals < cost:
        return await m.reply(f"❌ Not enough crystals. You need **{cost}** crystals.")

    beast_name = chat.beast_status['name']
    role = BEAST_INFO[beast_name]['Role']

    # Append beast to user's barracks based on its role.
    # If the beast isn't present, add it; if it's already there, prevent duplicate addition.
    if 'Protector' in role:
        if u.protectors.get(beast_name, 0) >= 1:
            return await m.reply("❌ You already have this protector beast!")
        u.protectors[beast_name] = 1
    elif 'Attacker' in role:
        if u.attackers.get(beast_name, 0) >= 1:
            return await m.reply("❌ You already have this attacker beast!")
        u.attackers[beast_name] = 1

    u.crystals -= cost
    chat.beast_status = None

    await asyncio.gather(
        u.update(),
        chat.update(),
        m.reply(f"🎉 **{m.from_user.first_name}** caught **{beast_name}** for {cost} crystals! 🦖")
    )

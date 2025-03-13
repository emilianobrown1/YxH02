from pyrogram import Client, filters
from ..Class.user import User
from . import YxH


# Beast information dictionary
BEAST_INFO = {
    "Titanus Aegisorn": {
        "Role": "Shield Guardian",
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
        "Role": "Treasure Guardian",
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
        "Role": "Crystal Guardian",
        "Powers": ["Frost Snow", "Thunder Storm", "Speed"],
        "Weakness": "Strength",
        "Image": "Beast/Glacelynx.jpg"
    },
    "Ignirax": {
        "Role": "The Shieldbreaker",
        "Powers": ["Fire", "Natural Ground"],
        "Weakness": "Aqua Jet, Strength",
        "Image": "Beast/Ignirax.jpg"
    }
}

@Client.on_message(filters.command("infox"))
@YxH()
async def beast_info(_, m, u):
    spl = m.text.split(maxsplit=1)
    if len(spl) < 2:
        return await m.reply("❌ Please specify a beast name. Example: `/infox Titanus Aegisorn`")

    beast_name = spl[1]
    beast_data = BEAST_INFO.get(beast_name)

    if not beast_data:
        return await m.reply("❌ Beast not found! Please check the name and try again.")

    powers_text = "\n".join([f"⚡ {power}" for power in beast_data["Powers"]])
    message = (
        f"\n🔥 **{beast_name}** 🔥\n"
        f"🛡 **Role:** {beast_data['Role']}\n\n"
        f"💥 **Powers:**\n{powers_text}\n\n"
        f"⚠️ **Weakness:** {beast_data['Weakness']}"
    )
    
    await m.reply_photo(beast_data["Image"], caption=message)
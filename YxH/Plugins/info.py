from pyrogram import Client, filters
from ..Class.user import User
from . import YxH

# Beast information dictionary
BEAST_INFO = {
    "Titanus Aegisorn": {
        "Name Meaning": "Titanus = Giant, Aegisorn = Shielded Guardian",
        "Role": "Shield Protector",
        "Lore": "Titanus Aegisorn, known as 'The Shield of the Ancients,' is a legendary guardian beast forged from the very core of the earth.",
        "Abilities": ["Aegis Barrier", "Earthquake Stomp", "Thorned Rampage"],
        "Weakness": "None specified",
        "Image": "Beast/Titanus"
    },
    "Ignirax": {
        "Name Meaning": "Ignis = Fire, Rax = Destroyer",
        "Role": "The Shieldbreaker",
        "Lore": "Ignirax, the Molten Annihilator, is the ultimate force of destruction, forged from the heart of an eternal volcanic storm. Born from the ashes of a forgotten war, Ignirax was created by an ancient civilization as a living siege weapon.",
        "Abilities": ["Lava Charge", "Magma Surge", "Obsidian Horn Thrust", "Volcanic Roar", "Infernal Wrath (Ultimate Ability)"],
        "Weakness": "Weak against water-based attacks and celestial magic.",
        "Image": "Beast/Ignirax"
    },
    "Voltaryn": {
        "Name Meaning": "Volt = Electricity, Aryn = Protector",
        "Role": "Guardian of the Storm",
        "Lore": "Deep within the Evergreen Highlands, where nature thrives in harmony with the elements, a sacred guardian watches over the land.",
        "Abilities": ["Thunder Shield", "Storm Dash", "Electric Claw Strike"],
        "Weakness": "Vulnerable to dark magic and shadow-based creatures.",
        "Image": "Beast/Voltiscar"
    }
}

@Client.on_message(filters.command("info"))
@YxH()
async def beast_info(_, m, u):
    spl = m.text.split(maxsplit=1)
    if len(spl) < 2:
        return await m.reply("❌ Please specify a beast name. Example: `/info Titanus Aegisorn`")
    
    beast_name = spl[1]
    beast_data = BEAST_INFO.get(beast_name)
    
    if not beast_data:
        return await m.reply("❌ Beast not found! Please check the name and try again.")
    
    abilities_text = "\n".join([f"🔹 {ability}" for ability in beast_data["Abilities"]])
    
    message = (
        f"**{beast_name}**\n"
        f"*({beast_data['Name Meaning']})*\n\n"
        f"🔹 **Role:** {beast_data['Role']}\n"
        f"📖 **Lore:** {beast_data['Lore']}\n\n"
        f"⚡ **Abilities:**\n{abilities_text}\n\n"
        f"⚠️ **Weakness:** {beast_data['Weakness']}"
    )
    
    await m.reply_photo(beast_data["Image"], caption=message)

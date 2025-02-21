from pyrogram import Client, filters from ..Class.user import User from . import YxH

Beast information dictionary

BEAST_INFO = { "Titanus Aegisorn": { "Name Meaning": "Titanus = Giant, Aegisorn = Shielded Guardian", "Role": "Shield Guardian", "Lore": "Titanus Aegisorn, known as 'The Shield of the Ancients,' is a legendary guardian beast forged from the very core of the earth.", "Powers": ["Aqua Jet", "Natural Ground"], "Weakness": "Flame Heat Inferno", "Image": "Beast/Titanus.jpg" }, "Voltaryn": { "Name Meaning": "Volt = Electricity, Aryn = Protector", "Role": "Collection Protector", "Lore": "Deep within the Evergreen Highlands, where nature thrives in harmony with the elements, a sacred guardian watches over the land.", "Powers": ["Thunder Storm", "Darkness Shadow"], "Weakness": "Natural Ground", "Image": "Beast/Voltaryn.jpg" }, "Cerberus": { "Name Meaning": "Cerberus = Mythical Guardian of the Underworld", "Role": "Treasure Guardian", "Lore": "A fearsome three-headed beast, standing as the eternal guardian of hidden treasures and lost relics.", "Powers": ["Flame Heat Inferno", "Darkness Shadow"], "Weakness": "None specified", "Image": "Beast/Cerberus.jpg" }, "Vilescale": { "Name Meaning": "Vile = Corrupt, Scale = Serpent", "Role": "Collection Attacker", "Lore": "A venomous terror lurking in the shadows, Vilescale strikes swiftly and without mercy.", "Powers": ["Venom", "Natural Ground"], "Weakness": "Lightning, Darkness Shadow", "Image": "Beast/Vilescale.jpg" }, "Frostclaw": { "Name Meaning": "Frost = Ice, Claw = Predator", "Role": "Crystal Attacker", "Lore": "Born in the frozen tundras, Frostclaw dominates the battlefield with icy precision.", "Powers": ["Strength", "Frost Snow"], "Weakness": "Speed, Thunder Storm, Darkness Shadow", "Image": "Beast/Frostclaw.jpg" }, "Phoenix": { "Name Meaning": "Phoenix = Immortal Firebird", "Role": "Treasury Attacker", "Lore": "A legendary firebird reborn from its own ashes, leaving a trail of destruction in its wake.", "Powers": ["Darkness Shadow", "Flame Heat Inferno"], "Weakness": "Speed, Natural Ground", "Image": "Beast/Phoenix.jpg" }, "Glacelynx": { "Name Meaning": "Glace = Ice, Lynx = Agile Hunter", "Role": "Crystal Guardian", "Lore": "A swift and cunning guardian of the frozen crystals, defending them against all who dare approach.", "Powers": ["Frost Snow", "Thunder Storm", "Speed"], "Weakness": "Strength", "Image": "Beast/Glacelynx.jpg" }, "Ignirax": { "Name Meaning": "Ignis = Fire, Rax = Destroyer", "Role": "The Shieldbreaker", "Lore": "Ignirax, the Molten Annihilator, is the ultimate force of destruction, forged from the heart of an eternal volcanic storm.", "Powers": ["Fire", "Natural Ground"], "Weakness": "Aqua Jet, Strength", "Image": "Beast/Ignirax.jpg" } }

@Client.on_message(filters.command("infox")) @YxH() async def beast_info(_, m, u): spl = m.text.split(maxsplit=1) if len(spl) < 2: return await m.reply("❌ Please specify a beast name. Example: /infox Titanus Aegisorn")

beast_name = spl[1]
beast_data = BEAST_INFO.get(beast_name)

if not beast_data:
    return await m.reply("❌ Beast not found! Please check the name and try again.")

powers_text = "\n".join([f"⚡ {power}" for power in beast_data["Powers"]])
message = (
    f"\n🔥 **{beast_name}** 🔥\n"
    f"✨ *({beast_data['Name Meaning']})* ✨\n\n"
    f"🛡 **Role:** {beast_data['Role']}\n"
    f"📜 **Lore:** {beast_data['Lore']}\n\n"
    f"💥 **Powers:**\n{powers_text}\n\n"
    f"⚠️ **Weakness:** {beast_data['Weakness']}"
)

await m.reply_photo(beast_data["Image"], caption=message)


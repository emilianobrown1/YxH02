from pyrogram import Client, filters
from . import get_user, YxH
import time, random

@Client.on_message(filters.command("comboattack"))
@YxH()
async def comboattack(_, m, u):
    # Must belong to a clan
    if not u.clan_id:
        return await m.reply("You must be part of a clan to attack.")

    # Determine target user ID
    if m.reply_to_message:
        target_user_id = m.reply_to_message.from_user.id
    else:
        parts = m.text.strip().split()
        if len(parts) >= 3 and parts[2].isdigit():
            target_user_id = int(parts[2])
        else:
            return await m.reply("Usage: reply to a user or `/comboattack <type> <user_id>`")

    t = await get_user(target_user_id)

    # Cannot attack same clan
    if u.clan_id == t.clan_id:
        return await m.reply("You cannot attack your clan mates.")

    # Respect defend cooldown (3 hours)
    if t.latest_defend and (time.time() - t.latest_defend) <= 10800:
        return await m.reply("Target user was attacked recently. Try again later.")

    # Parse attack type (default to 'shield' if reply-only)
    if len(m.command) >= 2:
        attack_type = m.command[1].lower()
    else:
        attack_type = "shield"

    # --- SHIELD ATTACK ---
    if attack_type == "shield":
        # Protector check
        if t.protectors.get("Titanus Aegisorn", 0) > 0:
            if u.attackers.get("Ignirax", 0) > 0:
                u.attackers["Ignirax"] -= 1
            t.protectors["Titanus Aegisorn"] = max(0, t.protectors["Titanus Aegisorn"] - 1)
            await u.update(); await t.update()
            return await m.reply(
                "Attack blocked: Shield Guardian (Titanus Aegisorn) countered you. "
                "Ignirax and the protector each lose 1."
            )

        # Expire any old shield
        if t.shield and (time.time() - t.shield[1]) > t.shield[0]:
            t.shield = []

        # Troop & power requirements
        if u.troops.get("shinobi", 0) < 15 or u.troops.get("wizard", 0) < 10 or u.troops.get("sensei", 0) < 5:
            return await m.reply("Not enough troops: need 15 Shinobi, 10 Wizard, 5 Sensei.")
        if u.power.get("Flame Heat Inferno", 0) <= 0 or u.power.get("Nature Ground", 0) <= 0:
            return await m.reply("Need powers: Flame Heat Inferno & Nature Ground.")
        if u.attackers.get("Ignirax", 0) <= 0:
            return await m.reply("Need attacker beast: Ignirax.")

        # Execute attack
        loot_gems     = int(t.gems     * 0.50)
        loot_gold     = int(t.gold     * 0.50)
        loot_crystals = int(t.crystals * 0.20)

        t.gems     = max(0, t.gems     - loot_gems)
        t.gold     = max(0, t.gold     - loot_gold)
        t.crystals = max(0, t.crystals - loot_crystals)

        u.gems     += loot_gems
        u.gold     += loot_gold
        u.crystals += loot_crystals

        # Consume attacker, troops & powers
        u.attackers["Ignirax"]   = max(0, u.attackers["Ignirax"] - 1)
        u.troops.update({"shinobi":0, "wizard":0, "sensei":0})
        u.power.update({"Flame Heat Inferno":0, "Nature Ground":0})

        t.latest_defend = time.time()
        await u.update(); await t.update()

        return await m.reply(
            f"Shield combo attack successful! Looted: {loot_gold} Gold, {loot_gems} Gems, {loot_crystals} Crystals."
        )

    # --- CRYSTAL ATTACK ---
    elif attack_type in ("crystal", "crystals"):
        if t.protectors.get("Glacelynx", 0) > 0:
            if u.attackers.get("Frostclaw", 0) > 0:
                u.attackers["Frostclaw"] -= 1
            t.protectors["Glacelynx"] = max(0, t.protectors["Glacelynx"] - 1)
            await u.update(); await t.update()
            return await m.reply(
                "Blocked by Crystal Guardian (Glacelynx). "
                "Frostclaw and the protector each lose 1."
            )

        if u.crystals < 3:
            return await m.reply("Need 3 Crystals to perform Crystal attack.")
        if u.troops.get("shinobi", 0) < 10 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 15:
            return await m.reply("Not enough troops: 10 Shinobi, 15 Wizard, 15 Sensei.")
        if u.power.get("Strength", 0) <= 0 or u.power.get("Frost Snow", 0) <= 0:
            return await m.reply("Need powers: Strength & Frost Snow.")
        if u.attackers.get("Frostclaw", 0) <= 0:
            return await m.reply("Need attacker beast: Frostclaw.")

        u.crystals -= 3
        loot_base    = int(t.crystals * 0.30)
        loot_extra   = int(t.treasure[2] * 0.30)
        t.crystals   = max(0, t.crystals - loot_base)
        t.treasure[2]= max(0, t.treasure[2] - loot_extra)

        total_loot = loot_base + loot_extra
        u.crystals += total_loot

        u.attackers["Frostclaw"] = max(0, u.attackers["Frostclaw"] - 1)
        u.troops.update({"shinobi":0, "wizard":0, "sensei":0})
        u.power.update({"Strength":0, "Frost Snow":0})

        t.latest_defend = time.time()
        await u.update(); await t.update()

        return await m.reply(
            f"Crystal combo attack successful! Looted {total_loot} Crystals."
        )

    # --- COLLECTION ATTACK ---
    elif attack_type == "collection":
        if t.protectors.get("Voltaryn", 0) > 0:
            if u.attackers.get("Vilescale", 0) > 0:
                u.attackers["Vilescale"] -= 1
            t.protectors["Voltaryn"] = max(0, t.protectors["Voltaryn"] - 1)
            await u.update(); await t.update()
            return await m.reply(
                "Blocked by Collection Protector (Voltaryn). "
                "Vilescale and the protector each lose 1."
            )

        if u.troops.get("shinobi", 0) < 10 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 10:
            return await m.reply("Not enough troops: 10 Shinobi, 15 Wizard, 10 Sensei.")
        if u.power.get("Thunder Storm", 0) <= 0 or u.power.get("Nature Ground", 0) <= 0:
            return await m.reply("Need powers: Thunder Storm & Nature Ground.")
        if u.attackers.get("Vilescale", 0) <= 0:
            return await m.reply("Need attacker beast: Vilescale.")

        # Steal up to 5 characters
        available = list(t.collection.keys())
        loot = random.sample(available, min(5, len(available))) if available else []
        for char in loot:
            u.collection[char] = t.collection.pop(char)

        u.attackers["Vilescale"] = max(0, u.attackers["Vilescale"] - 1)
        u.troops.update({"shinobi":0, "wizard":0, "sensei":0})
        u.power.update({"Thunder Storm":0, "Nature Ground":0})

        t.latest_defend = time.time()
        await u.update(); await t.update()

        if loot:
            return await m.reply(
                f"Collection combo attack successful! Looted characters: {', '.join(map(str, loot))}."
            )
        else:
            return await m.reply("Collection attack successful but no characters to loot.")

    # --- TREASURE ATTACK ---
    elif attack_type == "treasure":
        if t.protectors.get("Cerberus", 0) > 0:
            if u.attackers.get("Pyraxion", 0) > 0:
                u.attackers["Pyraxion"] -= 1
            t.protectors["Cerberus"] = max(0, t.protectors["Cerberus"] - 1)
            await u.update(); await t.update()
            return await m.reply(
                "Blocked by Treasure Guardian (Cerberus). "
                "Pyraxion and the protector each lose 1."
            )

        if u.troops.get("shinobi", 0) < 15 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 10:
            return await m.reply("Not enough troops: 15 Shinobi, 15 Wizard, 10 Sensei.")
        if u.power.get("Darkness Shadow", 0) <= 0 or u.power.get("Flame Heat Inferno", 0) <= 0:
            return await m.reply("Need powers: Darkness Shadow & Flame Heat Inferno.")
        if u.attackers.get("Pyraxion", 0) <= 0:
            return await m.reply("Need attacker beast: Pyraxion.")

        loot_gold     = int(t.treasure[0] * 0.40)
        loot_gems     = int(t.treasure[1] * 0.40)
        loot_crystals = int(t.treasure[2] * 0.30)

        t.treasure[0] = max(0, t.treasure[0] - loot_gold)
        t.treasure[1] = max(0, t.treasure[1] - loot_gems)
        t.treasure[2] = max(0, t.treasure[2] - loot_crystals)

        u.gold     += loot_gold
        u.gems     += loot_gems
        u.crystals += loot_crystals

        u.attackers["Pyraxion"] = max(0, u.attackers["Pyraxion"] - 1)
        u.troops.update({"shinobi":0, "wizard":0, "sensei":0})
        u.power.update({"Darkness Shadow":0, "Flame Heat Inferno":0})

        t.latest_defend = time.time()
        await u.update(); await t.update()

        return await m.reply(
            f"Treasure combo attack successful! Looted: {loot_gold} Gold, {loot_gems} Gems, {loot_crystals} Crystals."
        )

    # --- INVALID TYPE ---
    else:
        return await m.reply(
            "Invalid attack type. Use: shield, crystal(s), collection, or treasure."
            )

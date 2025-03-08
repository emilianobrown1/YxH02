from pyrogram import Client, filters
from . import get_user, YxH
import time, random

@Client.on_message(filters.command("comboattack"))
@YxH()
async def comboattack(_, m, u):
    if not u.clan_id:
        return await m.reply("You must be part of a clan to attack.")
    
    if not m.reply_to_message:
        return await m.reply("Reply to a user's message to attack.")
    
    t = await get_user(m.reply_to_message.from_user.id)
    if u.clan_id == t.clan_id:
        return await m.reply("You cannot attack your clan mates.")
    
    if t.latest_defend and int(time.time() - t.latest_defend) <= 10800:
        return await m.reply("Target user was attacked recently. Try again later.")
    
    try:
        attack_type = m.command[1].lower()
    except IndexError:
        attack_type = "shield"
    
    if attack_type == "shield":
        if t.protectors.get("Titanus Aegisorn", 0) > 0:
            return await m.reply("Target is protected by Shield Guardian (Titanus Aegisorn).")
        
        if t.shield:
            if int(time.time() - t.shield[1]) <= t.shield[0]:
                t.shield = []
        
        if u.troops.get("shinobi", 0) < 15 or u.troops.get("wizard", 0) < 10 or u.troops.get("sensei", 0) < 5:
            return await m.reply("Not enough troops for shield attack. Required: 15 Shinobis, 10 Wizards, 5 Sensei.")
        
        if u.power.get("Flame Heat Inferno", 0) <= 0 or u.power.get("Nature Ground", 0) <= 0:
            return await m.reply("You do not meet the power requirements for shield attack (Fire & Natural Ground).")
        
        if u.attackers.get("Ignirax", 0) <= 0:
            return await m.reply("You do not have the required beast (Ignirax) for shield attack.")
        
        loot_gems = int(t.gems * 0.50)
        loot_gold = int(t.gold * 0.50)
        loot_crystals = int(t.crystals * 0.20)
        
        t.gems = max(0, t.gems - loot_gems)
        t.gold = max(0, t.gold - loot_gold)
        t.crystals = max(0, t.crystals - loot_crystals)
        
        u.gems += loot_gems
        u.gold += loot_gold
        u.crystals += loot_crystals
        
        t.latest_defend = time.time()
        await u.update()
        await t.update()
        
        return await m.reply(
            f"Shield combo attack executed successfully.\nLooted: {loot_gold} Gold, {loot_gems} Gems, {loot_crystals} Crystals."
        )
    
    elif attack_type in ["crystal", "crystals"]:
        if t.protectors.get("Glacelynx", 0) > 0:
            return await m.reply("Target is protected by Crystal Guardian (Glacelynx).")
        
        if u.crystals < 35:
            return await m.reply("You do not have enough crystals (35 required) to perform this attack.")
        
        if u.troops.get("shinobi", 0) < 10 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 15:
            return await m.reply("Not enough troops for crystal attack. Required: 10 Shinobis, 15 Wizards, 15 Sensei.")
        
        if u.power.get("Strength", 0) <= 0 or u.power.get("Frost Snow", 0) <= 0:
            return await m.reply("You do not meet the power requirements for crystal attack (Strength & Frost Snow).")
        
        if u.attackers.get("Frostclaw", 0) <= 0:
            return await m.reply("You do not have the required beast (Frostclaw) for crystal attack.")
        
        u.crystals -= 35
        
        loot_normal = int(t.crystals * 0.30)
        loot_treasure = int(t.treasure[2] * 0.30)
        t.crystals = max(0, t.crystals - loot_normal)
        t.treasure[2] = max(0, t.treasure[2] - loot_treasure)
        total_loot = loot_normal + loot_treasure
        u.crystals += total_loot
        
        t.latest_defend = time.time()
        await u.update()
        await t.update()
        
        return await m.reply(
            f"Crystal combo attack executed successfully.\nLooted: {loot_normal} crystals and {loot_treasure} treasure crystals (Total: {total_loot})."
        )
    
    elif attack_type == "collection":
        if t.protectors.get("Voltiscar", 0) > 0:
            return await m.reply("Target is protected by Collection Protector (Voltiscar).")
        
        if u.troops.get("shinobi", 0) < 10 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 10:
            return await m.reply("Not enough troops for collection attack. Required: 10 Shinobis, 15 Wizards, 10 Sensei.")
        
        # Corrected power check: Replaced "Venom" with "Thunder Storm"
        if u.power.get("Thunder Storm", 0) <= 0 or u.power.get("Nature Ground", 0) <= 0:
            return await m.reply("You do not meet the power requirements for collection attack (Thunder Storm & Natural Ground).")
        
        if u.attackers.get("Vilescale", 0) <= 0:
            return await m.reply("You do not have the required beast (Vilescale) for collection attack.")
        
        available_chars = list(t.collection.keys())
        loot_chars = random.sample(available_chars, min(3, len(available_chars))) if available_chars else []
        
        for char in loot_chars:
            u.collection[char] = t.collection.pop(char)
        
        t.latest_defend = time.time()
        await u.update()
        await t.update()
        
        if loot_chars:
            return await m.reply(f"Collection combo attack executed successfully.\nLooted characters: {', '.join(loot_chars)}")
        else:
            return await m.reply("Collection combo attack executed, but target has no characters in their collection.")
    
    elif attack_type == "treasure":
        if t.protectors.get("Cerberus", 0) > 0:
            return await m.reply("Target is protected by Treasure Guardian (Cerberus).")
        
        if u.troops.get("shinobi", 0) < 15 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 10:
            return await m.reply("Not enough troops for treasure attack. Required: 15 Shinobis, 15 Wizards, 10 Sensei.")
        
        if u.power.get("Darkness Shadow", 0) <= 0 or u.power.get("Flame Heat Inferno", 0) <= 0:
            return await m.reply("You do not meet the power requirements for treasure attack (Darkness Shadow & Flame Heat Inferno).")
        
        # Corrected attacker check: Replaced "Phoenix" with "Pyraxion"
        if u.attackers.get("Pyraxion", 0) <= 0:
            return await m.reply("You do not have the required beast (Pyraxion) for treasure attack.")
        
        loot_treasure_gold = int(t.treasure[0] * 0.40)
        loot_treasure_gems = int(t.treasure[1] * 0.40)
        loot_treasure_crystals = int(t.treasure[2] * 0.30)
        
        t.treasure[0] = max(0, t.treasure[0] - loot_treasure_gold)
        t.treasure[1] = max(0, t.treasure[1] - loot_treasure_gems)
        t.treasure[2] = max(0, t.treasure[2] - loot_treasure_crystals)
        
        u.gold += loot_treasure_gold
        u.gems += loot_treasure_gems
        u.crystals += loot_treasure_crystals
        
        t.latest_defend = time.time()
        await u.update()
        await t.update()
        
        return await m.reply(
            f"Treasure combo attack executed successfully.\nLooted from treasure: {loot_treasure_gold} Gold, {loot_treasure_gems} Gems, {loot_treasure_crystals} Crystals."
        )
    
    else:
        return await m.reply("Invalid attack type. Please use one of: shield, crystals (or crystal), collection, treasure.")

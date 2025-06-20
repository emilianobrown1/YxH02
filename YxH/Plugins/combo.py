from pyrogram import Client, filters
from . import get_user, YxH
import time, random

@Client.on_message(filters.command("comboattack")) @YxH() async def comboattack(_, m, u): if not u.clan_id: return await m.reply("❌ ʏᴏᴜ ᴍᴜꜱᴛ ʙᴇ ᴘᴀʀᴛ ᴏꜰ ᴀ ᴄʟᴀɴ ᴛᴏ ᴀᴛᴛᴀᴄᴋ.")

if m.reply_to_message:
    target_user_id = m.reply_to_message.from_user.id
else:
    parts = m.text.strip().split()
    if len(parts) >= 3 and parts[2].isdigit():
        target_user_id = int(parts[2])
    else:
        return await m.reply("⚔️ ᴜꜱᴀɢᴇ: ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ `/comboattack <type> <user_id>`")

t = await get_user(target_user_id)

if u.clan_id == t.clan_id:
    return await m.reply("🚫 ʏᴏᴜ ᴄᴀɴɴᴏᴛ ᴀᴛᴛᴀᴄᴋ ʏᴏᴜʀ ᴄʟᴀɴ ᴍᴀᴛᴇꜱ.")
if t.latest_defend and (time.time() - t.latest_defend) <= 10800:
    return await m.reply("🛡️ ᴛᴀʀɢᴇᴛ ᴡᴀꜱ ʀᴇᴄᴇɴᴛʟʏ ᴀᴛᴛᴀᴄᴋᴇᴅ. ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")

attack_type = m.command[1].lower() if len(m.command) >= 2 else "shield"

# Shield attack already updated earlier...

# CRYSTAL ATTACK
elif attack_type in ("crystal", "crystals"):
    if t.protectors.get("Glacelynx", 0) > 0:
        if u.attackers.get("Frostclaw", 0) > 0:
            u.attackers["Frostclaw"] -= 1
        t.protectors["Glacelynx"] = max(0, t.protectors["Glacelynx"] - 1)
        await u.update(); await t.update()
        return await m.reply("🧊 ʙʟᴏᴄᴋᴇᴅ ʙʏ ᴄʀʏꜱᴛᴀʟ ɢᴜᴀʀᴅɪᴀɴ (ɢʟᴀᴄᴇʟʏɴx).")

    if u.crystals < 3:
        return await m.reply("💠 ɴᴇᴇᴅ 3 ᴄʀʏꜱᴛᴀʟꜱ ꜰᴏʀ ᴛʜɪꜱ ᴀᴛᴛᴀᴄᴋ.")
    if u.troops.get("shinobi", 0) < 10 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 15:
        return await m.reply("👥 ɴᴇᴇᴅ: 10 ꜱʜɪɴᴏʙɪ, 15 ᴡɪᴢᴀʀᴅ, 15 ꜱᴇɴꜱᴇɪ.")
    if u.power.get("Strength", 0) <= 0 or u.power.get("Frost Snow", 0) <= 0:
        return await m.reply("✨ ᴍɪꜱꜱɪɴɢ ᴘᴏᴡᴇʀꜱ: ꜱᴛʀᴇɴɢᴛʜ & ꜰʀᴏꜱᴛ ꜱɴᴏᴡ.")
    if u.attackers.get("Frostclaw", 0) <= 0:
        return await m.reply("❄️ ᴍɪꜱꜱɪɴɢ ᴀᴛᴛᴀᴄᴋᴇʀ: ꜰʀᴏꜱᴛᴄʟᴀᴡ.")

    u.crystals -= 3
    loot_base = int(t.crystals * 0.30)
    loot_extra = int(t.treasure[2] * 0.30)
    total_loot = loot_base + loot_extra

    t.crystals -= loot_base
    t.treasure[2] -= loot_extra
    u.crystals += total_loot

    u.attackers["Frostclaw"] -= 1
    u.troops.update({"shinobi": 0, "wizard": 0, "sensei": 0})
    u.power.update({"Strength": 0, "Frost Snow": 0})

    t.latest_defend = time.time()
    await u.update(); await t.update()

    await m.reply(f"✅ ᴄʀʏꜱᴛᴀʟ ᴄᴏᴍʙᴏ ᴀᴛᴛᴀᴄᴋ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ! ʟᴏᴏᴛᴇᴅ `{total_loot}` ᴄʀʏꜱᴛᴀʟꜱ.")
    try:
        await _.send_message(
            t.user.id,
            f"⚠️ **{u.user.first_name}** ᴜꜱᴇᴅ *ᴄʀʏꜱᴛᴀʟ ᴄᴏᴍʙᴏ ᴀᴛᴛᴀᴄᴋ*!\n"
            f"ʟᴏꜱᴛ: `{total_loot}` ᴄʀʏꜱᴛᴀʟꜱ."
        )
    except:
        pass

# COLLECTION ATTACK
elif attack_type == "collection":
    if t.protectors.get("Voltaryn", 0) > 0:
        if u.attackers.get("Vilescale", 0) > 0:
            u.attackers["Vilescale"] -= 1
        t.protectors["Voltaryn"] = max(0, t.protectors["Voltaryn"] - 1)
        await u.update(); await t.update()
        return await m.reply("📦 ʙʟᴏᴄᴋᴇᴅ ʙʏ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴘʀᴏᴛᴇᴄᴛᴏʀ (ᴠᴏʟᴛᴀʀʏɴ).")

    if u.troops.get("shinobi", 0) < 10 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 10:
        return await m.reply("👥 ɴᴇᴇᴅ: 10 ꜱʜɪɴᴏʙɪ, 15 ᴡɪᴢᴀʀᴅ, 10 ꜱᴇɴꜱᴇɪ.")
    if u.power.get("Thunder Storm", 0) <= 0 or u.power.get("Nature Ground", 0) <= 0:
        return await m.reply("⚡ ᴍɪꜱꜱɪɴɢ ᴘᴏᴡᴇʀꜱ: ᴛʜᴜɴᴅᴇʀ ꜱᴛᴏʀᴍ & ɴᴀᴛᴜʀᴇ ɢʀᴏᴜɴᴅ.")
    if u.attackers.get("Vilescale", 0) <= 0:
        return await m.reply("🐍 ᴍɪꜱꜱɪɴɢ ᴀᴛᴛᴀᴄᴋᴇʀ: ᴠɪʟᴇꜱᴄᴀʟᴇ.")

    available = list(t.collection.keys())
    loot = random.sample(available, min(5, len(available))) if available else []
    for char in loot:
        u.collection[char] = t.collection.pop(char)

    u.attackers["Vilescale"] -= 1
    u.troops.update({"shinobi": 0, "wizard": 0, "sensei": 0})
    u.power.update({"Thunder Storm": 0, "Nature Ground": 0})

    t.latest_defend = time.time()
    await u.update(); await t.update()

    if loot:
        await m.reply(f"✅ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴀᴛᴛᴀᴄᴋ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ! ʟᴏᴏᴛᴇᴅ: {', '.join(map(str, loot))}.")
        try:
            await _.send_message(
                t.user.id,
                f"⚠️ **{u.user.first_name}** ᴜꜱᴇᴅ *ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴀᴛᴛᴀᴄᴋ*!\nʟᴏꜱᴛ: {', '.join(map(str, loot))}"
            )
        except:
            pass
    else:
        await m.reply("✅ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴀᴛᴛᴀᴄᴋ ᴅᴏɴᴇ, ʙᴜᴛ ɴᴏ ᴄʜᴀʀᴀᴄᴛᴇʀꜱ ᴛᴏ ʟᴏᴏᴛ.")

# TREASURE ATTACK
elif attack_type == "treasure":
    if t.protectors.get("Cerberus", 0) > 0:
        if u.attackers.get("Pyraxion", 0) > 0:
            u.attackers["Pyraxion"] -= 1
        t.protectors["Cerberus"] = max(0, t.protectors["Cerberus"] - 1)
        await u.update(); await t.update()
        return await m.reply("🐲 ʙʟᴏᴄᴋᴇᴅ ʙʏ ᴛʀᴇᴀꜱᴜʀᴇ ɢᴜᴀʀᴅɪᴀɴ (ᴄᴇʀʙᴇʀᴜꜱ).")

    if u.troops.get("shinobi", 0) < 15 or u.troops.get("wizard", 0) < 15 or u.troops.get("sensei", 0) < 10:
        return await m.reply("👥 ɴᴇᴇᴅ: 15 ꜱʜɪɴᴏʙɪ, 15 ᴡɪᴢᴀʀᴅ, 10 ꜱᴇɴꜱᴇɪ.")
    if u.power.get("Darkness Shadow", 0) <= 0 or u.power.get("Flame Heat Inferno", 0) <= 0:
        return await m.reply("🔥 ᴍɪꜱꜱɪɴɢ ᴘᴏᴡᴇʀꜱ: ᴅᴀʀᴋɴᴇꜱꜱ ꜱʜᴀᴅᴏᴡ & ꜰʟᴀᴍᴇ ʜᴇᴀᴛ ɪɴꜰᴇʀɴᴏ.")
    if u.attackers.get("Pyraxion", 0) <= 0:
        return await m.reply("🐉 ᴍɪꜱꜱɪɴɢ ᴀᴛᴛᴀᴄᴋᴇʀ: ᴘʏʀᴀxɪᴏɴ.")

    loot_gold = int(t.treasure[0] * 0.40)
    loot_gems = int(t.treasure[1] * 0.40)
    loot_crystals = int(t.treasure[2] * 0.30)

    t.treasure[0] -= loot_gold
    t.treasure[1] -= loot_gems
    t.treasure[2] -= loot_crystals

    u.gold += loot_gold
    u.gems += loot_gems
    u.crystals += loot_crystals

    u.attackers["Pyraxion"] -= 1
    u.troops.update({"shinobi": 0, "wizard": 0, "sensei": 0})
    u.power.update({"Darkness Shadow": 0, "Flame Heat Inferno": 0})

    t.latest_defend = time.time()
    await u.update(); await t.update()

    await m.reply(f"✅ ᴛʀᴇᴀꜱᴜʀᴇ ᴀᴛᴛᴀᴄᴋ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ! ʟᴏᴏᴛᴇᴅ: `{loot_gold}` ɢᴏʟᴅ, `{loot_gems}` ɢᴇᴍꜱ, `{loot_crystals}` ᴄʀʏꜱᴛᴀʟꜱ.")
    try:
        await _.send_message(
            t.user.id,
            f"⚠️ **{u.user.first_name}** ᴜꜱᴇᴅ *ᴛʀᴇᴀꜱᴜʀᴇ ᴄᴏᴍʙᴏ ᴀᴛᴛᴀᴄᴋ*!\n"
            f"ʟᴏꜱᴛ: `{loot_gold}` ɢᴏʟᴅ, `{loot_gems}` ɢᴇᴍꜱ, `{loot_crystals}` ᴄʀʏꜱᴛᴀʟꜱ."
        )
    except:
        pass

else:
    return await m.reply("⚠️ ɪɴᴠᴀʟɪᴅ ᴀᴛᴛᴀᴄᴋ ᴛʏᴘᴇ. ᴜꜱᴇ: shield, crystal, collection, or treasure.")


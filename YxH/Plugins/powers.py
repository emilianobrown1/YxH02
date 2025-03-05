from pyrogram import Client, filters
import random
import time
from ..Database.users import get_user
from ..universal_decorator import YxH

# Internal power quest tracker
active_quests = {}
last_message_time = {}  # Prevent spam tracking

POWER_NAMES = [
    "Darkness Shadow", "Frost Snow", "Thunder Storm",
    "Nature Ground", "Flame Heat Inferno", "Aqua Jet",
    "Strength", "Speed"
]

@Client.on_message(filters.command("search_power"))
@YxH()
async def start_power_quest(_, m, user):
    user_id = user.user.id

    if user.barracks_count == 0:
        await m.reply("🏰 You need to build a barrack before searching for power!")
        return

    if active_quests.get(user_id, {}).get('active'):
        await m.reply("🚀 You already have an active power quest! Use `/power_status` to check progress.")
        return

    active_quests[user_id] = {
        'active': True,
        'messages': 0,
        'discovered_power': None,
        'cost': 0
    }
    
    await m.reply(
        "🔮 **Power Quest Initiated!**\n\n"
        "Send 50 messages (non-commands) in any group to uncover ancient powers!\n"
        "✨ Each message brings you closer to legendary energy!\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "📊 Track progress: `/power_status`\n"
        "⚡ Claim power: `/get_power`"
    )

@Client.on_message(filters.command("get_power"))
@YxH()
async def claim_power(_, m, user):
    user_id = user.user.id
    quest = active_quests.get(user_id, {})
    
    if not quest.get('discovered_power'):
        await m.reply("❌ No power discovered! Complete a quest with `/search_power` first.")
        return

    if user.gems < quest['cost']:
        await m.reply(f"💎 Insufficient gems! Need {quest['cost']} gems.")
        return

    max_power = 3 * user.barracks_count
    current_total_power = sum(user.power.values())  # Get total power across all types
    
    if current_total_power >= max_power:
        await m.reply(f"⚠️ Max power capacity reached! (Max: {max_power})")
        return

    # Deduct gems and add power
    user.gems -= quest['cost']
    power_name = quest['discovered_power']
    user.power[power_name] = user.power.get(power_name, 0) + 1
    
    await user.update()
    del active_quests[user_id]
    
    await m.reply(
        f"⚡ **{power_name} Absorption Complete!**\n\n"
        f"🌀 Power Level: {user.power[power_name]}/{max_power}\n"
        f"💎 Energy Cost: {quest['cost']} gems\n"
        "🌌 Your troops surge with new energy!"
    )

@Client.on_message(filters.command("power_status"))
@YxH()
async def quest_status(_, m, user):
    user_id = user.user.id
    quest = active_quests.get(user_id, {})
    
    if quest.get('active'):
        remaining = 50 - quest['messages']
        await m.reply(
            f"📡 **Quest Progress:** {quest['messages']}/50 messages\n"
            f"🔋 Remaining: {remaining}\n"
            "💬 Keep chatting to unlock power!"
        )
    elif quest.get('discovered_power'):
        await m.reply(
            f"🌟 **Discovered Power:** {quest['discovered_power']}\n"
            f"💎 Claim Cost: {quest['cost']} gems\n"
            "Use `/get_power` to harness this energy!"
        )
    else:
        await m.reply(
            "🌌 **No Active Quest**\n"
            "Start your power journey with `/search_power`!"
        )

@Client.on_message(filters.group & filters.command)
async def track_messages(_, m):
    if not m.text or not m.from_user:
        return

    user_id = m.from_user.id
    quest = active_quests.get(user_id, {})

    if quest.get('active'):
        # Prevent spam tracking (5-second cooldown)
        current_time = time.time()
        if user_id in last_message_time and (current_time - last_message_time[user_id] < 5):
            return  # Ignore messages too close together

        last_message_time[user_id] = current_time  # Update last message time
        active_quests[user_id]['messages'] += 1

        if active_quests[user_id]['messages'] >= 50:
            active_quests[user_id].update({
                'active': False,
                'discovered_power': random.choice(POWER_NAMES),
                'cost': random.randint(35000, 85000)
            })
            
            try:
                await m.reply(
                    "🌀 **Power Source Detected!**\n\n"
                    f"💫 Discovered: {active_quests[user_id]['discovered_power']}\n"
                    f"⚡ Energy Cost: {active_quests[user_id]['cost']} gems\n"
                    "Use `/get_power` to claim it!"
                )
            except Exception as e:
                print(f"Error sending discovery notice: {e}")
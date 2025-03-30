from pyrogram import Client, filters
import random
import time
from ..Database.users import get_user
from ..Database.quest import save_quest_data, get_quest_data, delete_quest_data
from ..universal_decorator import YxH

active_quests = {}
last_message_time = {}  # Prevent spam tracking

POWER_NAMES = [
    "Darkness Shadow", "Frost Snow", "Thunder Storm",
    "Nature Ground", "Flame Heat Inferno", "Aqua Jet",
    "Strength", "Speed"
]

@Client.on_message(filters.command("search"))
@YxH()
async def start_power_quest(_, m, user):
    user_id = user.user.id

    if user.barracks_count == 0:
        await m.reply("🏰 You need to build a barrack before searching for power!")
        return

    # Attempt to load any existing quest from the database
    quest = await get_quest_data(user_id)
    if quest and quest.get('active'):
        active_quests[user_id] = quest
        await m.reply("🚀 You already have an active power quest! Use `/power_status` to check progress.")
        return

    # Otherwise, create a new quest state
    quest = {
        'active': True,
        'messages': 0,
        'discovered_power': None,
        'cost': 0
    }
    active_quests[user_id] = quest
    await save_quest_data(user_id, quest)

    await m.reply(
        "🔮 **Power Quest Initiated!**\n\n"
        "Send 200 messages (non-commands) in any group to uncover ancient powers!\n"
        "✨ Each message brings you closer to legendary energy!\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "📊 Track progress: `/power_status`\n"
        "⚡ Claim power: `/get_power`"
    )

async def track_messages(_, m):
    if not m.text or not m.from_user:
        return

    user_id = m.from_user.id
    quest = active_quests.get(user_id)
    
    if quest and quest.get('active'):
        current_time = time.time()
        if user_id in last_message_time and (current_time - last_message_time[user_id] < 5):
            return  # Ignore messages too close together

        last_message_time[user_id] = current_time
        quest['messages'] += 1

        # Update the persistent quest data
        await save_quest_data(user_id, quest)

        if quest['messages'] >= 200:
            quest.update({
                'active': False,
                'discovered_power': random.choice(POWER_NAMES),
                'cost': random.randint(35000, 85000)
            })
            await save_quest_data(user_id, quest)
            
            try:
                await m.reply(
                    "🌀 **Power Source Detected!**\n\n"
                    f"💫 Discovered: {quest['discovered_power']}\n"
                    f"⚡ Energy Cost: {quest['cost']} gems\n"
                    "Use `/get_power` to claim it!"
                )
            except Exception as e:
                print(f"Error sending discovery notice: {e}")

@Client.on_message(filters.command("getpower"))
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
    current_total_power = sum(user.power.values())
    
    if current_total_power >= max_power:
        await m.reply(f"⚠️ Max power capacity reached! (Max: {max_power})")
        return

    user.gems -= quest['cost']
    power_name = quest['discovered_power']
    user.power[power_name] = user.power.get(power_name, 0) + 1
    
    await user.update()
    
    # Remove quest state from memory and database
    if user_id in active_quests:
        del active_quests[user_id]
    await delete_quest_data(user_id)
    
    await m.reply(
        f"⚡ **{power_name} Absorption Complete!**\n\n"
        f"🌀 Power Level: {user.power[power_name]}/{max_power}\n"
        f"💎 Energy Cost: {quest['cost']} gems\n"
        "🌌 Your troops surge with new energy!"
    )

@Client.on_message(filters.command("status"))
@YxH()
async def quest_status(_, m, user):
    user_id = user.user.id
    # First try to get the quest from in-memory data
    quest = active_quests.get(user_id)
    # If not in memory, attempt to load from the database
    if not quest:
        quest = await get_quest_data(user_id)
        if quest:
            active_quests[user_id] = quest

    if quest:
        if quest.get('active'):
            remaining = 200 - quest['messages']
            await m.reply(
                f"📡 **Quest Progress:** {quest['messages']}/200 messages\n"
                f"🔋 Remaining: {remaining}\n"
                "💬 Keep chatting to unlock power!"
            )
        elif quest.get('discovered_power'):
            await m.reply(
                f"🌟 **Discovered Power:** {quest['discovered_power']}\n"
                f"💎 Claim Cost: {quest['cost']} gems\n"
                "Use `/getpower` to harness this energy!"
            )
        else:
            await m.reply(
                "🌌 **No Active Quest**\n"
                "Start your power journey with `/search`!"
            )
    else:
        await m.reply(
            "🌌 **No Active Quest**\n"
            "Start your power journey with `/search`!"
        )

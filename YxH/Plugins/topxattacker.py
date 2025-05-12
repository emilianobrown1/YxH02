from pyrogram import Client, filters
from database.attacks import get_top_attackers
from . import YxH

@Client.on_message(filters.command("topxattack"))
@YxH()
async def attack_leaderboard(_, m, u):
    leaderboard = await get_top_attackers()
    if not leaderboard:
        return await m.reply("No one has attacked yet.")

    text = "**Top Attackers Leaderboard**\n\n"
    for i, entry in enumerate(leaderboard, 1):
        name = entry.get("name", f"ID {entry['user_id']}")
        attack = entry.get("attack", 0)
        combo = entry.get("comboattack", 0)
        text += f"{i}. {name} — 🗡️ {attack} | ⚔️ {combo}\n"

    await m.reply(text)

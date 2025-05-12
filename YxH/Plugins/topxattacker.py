from database.attacks import get_top_attackers
from . import YxH, db  # Make sure `db` is imported

@Client.on_message(filters.command("topxattack"))
@YxH()
async def attack_leaderboard(_, m, u):
    leaderboard = await get_top_attackers()
    if not leaderboard:
        return await m.reply("No one has attacked yet.")

    text = "**Top Attackers Leaderboard**\n\n"
    for i, entry in enumerate(leaderboard, 1):
        user_id = entry["user_id"]
        attack = entry.get("attack", 0)
        combo = entry.get("comboattack", 0)

        # Try fetching username from users collection
        user_data = await db.users.find_one({"user_id": user_id})
        name = user_data.get("name") if user_data else f"ID {user_id}"

        text += f"{i}. {name} — 🗡️ {attack} | ⚔️ {combo}\n"

    await m.reply(text)
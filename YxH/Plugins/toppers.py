from pyrogram import Client, filters
from ..Database.users import get_all_users
from ..universal_decorator import YxH
import heapq

def get_display_name(user):
    name = getattr(user.user, "first_name", None) 
    if not name:
        name = getattr(user.user, "username", None) or f"User {user.user.id}"
    return name

def get_progress_bar(value, max_value, bar_length=10):
    if max_value == 0:
        return ""
    progress = value / max_value
    filled = int(round(progress * bar_length))
    return "█" * filled + "▁" * (bar_length - filled)

async def generate_leaderboard(title, emoji, users, key_func, value_format):
    sorted_users = sorted(users, key=key_func, reverse=True)
    top10 = sorted_users[:10]
    max_value = key_func(top10[0]) if top10 else 0
    current_user = next((u for u in sorted_users if u.user.id == users[0].user.id), None)

    txt = f"🏆 **{title} Leaderboard** {emoji}\n"
    txt += "═" * 35 + "\n\n"

    for idx, user in enumerate(top10):
        rank = idx + 1
        value = key_func(user)
        progress = get_progress_bar(value, max_value)

        rank_emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"▫️**{rank}**"
        highlight = " 👑" if user.user.id == current_user.user.id else ""

        txt += (
            f"{rank_emoji} **{get_display_name(user)}**{highlight}\n"
            f"┣ {value_format(value)} {progress}\n\n"
        )

    # Current user's rank
    if current_user and (current_user not in top10):
        user_rank = sorted_users.index(current_user) + 1
        user_value = key_func(current_user)
        progress = get_progress_bar(user_value, max_value)
        txt += (
            f"🎖️ **Your Rank**: #{user_rank}\n"
            f"┣ {value_format(user_value)} {progress}\n\n"
        )

    # Statistics footer
    total = len(users)
    avg_value = sum(key_func(u) for u in users) / total if total > 0 else 0
    txt += (
        f"📊 **Total Participants**: `{total}`\n"
        f"📈 **Average Value**: {value_format(avg_value)}"
    )

    return txt

@Client.on_message(filters.command("topx"))
@YxH()
async def top_miners(_, m, u):
    users = await get_all_users()
    response = await generate_leaderboard(
        title="Gold Miners",
        emoji="💰",
        users=users,
        key_func=lambda u: u.gold,
        value_format=lambda v: f"`{v:,}g`"
    )
    await m.reply(response)

@Client.on_message(filters.command("ctop"))
@YxH()
async def top_collectors(_, m, u):
    users = await get_all_users()
    response = await generate_leaderboard(
        title="Collection Masters",
        emoji="📦",
        users=users,
        key_func=lambda u: len(u.collection),
        value_format=lambda v: f"`{v} items`"
    )
    await m.reply(response)

@Client.on_message(filters.command("crtop"))
@YxH()
async def top_crystals(_, m, u):
    users = await get_all_users()
    response = await generate_leaderboard(
        title="Crystal Kings",
        emoji="💎",
        users=users,
        key_func=lambda u: u.crystals,
        value_format=lambda v: f"`{v:,} crystals`"
    )
    await m.reply(response)
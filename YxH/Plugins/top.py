from pyrogram import Client, filters
from ..Database.users import get_all_users

# Image paths for leaderboards
TOP_MINERS_IMAGE_PATH = "Images/mtop.jpg"
TOP_COLLECTORS_IMAGE_PATH = "Images/top.jpg"
TOP_CRYSTAL_HOLDERS_IMAGE_PATH = "Images/ctop.jpg"


async def get_top_users(attribute, top_limit=10):
    """
    Fetch all users and sort them based on the given attribute.
    """
    all_users = await get_all_users()
    # Sort users by the specified attribute (e.g., gold, crystals, collection size)
    sorted_users = sorted(all_users, key=lambda user: getattr(user, attribute, 0), reverse=True)
    return sorted_users[:top_limit]


@Client.on_message(filters.command("top"))
async def top_gold(_, message):
    """
    Command to show the top gold holders.
    Usage: /top
    """
    top_users = await get_top_users("gold", 10)
    leaderboard = "🏆 **Top 10 Gold Holders** 🏆\n"
    leaderboard += "\n".join(
        [f"{i + 1}. User {user.user}: {user.gold} Gold" for i, user in enumerate(top_users)]
    )
    await message.reply_photo(
        photo=TOP_MINERS_IMAGE_PATH,
        caption=leaderboard
    )


@Client.on_message(filters.command("crtop"))
async def top_crystals(_, message):
    """
    Command to show the top crystal holders.
    Usage: /crtop
    """
    top_users = await get_top_users("crystals", 10)
    leaderboard = "💎 **Top 10 Crystal Holders** 💎\n"
    leaderboard += "\n".join(
        [f"{i + 1}. User {user.user}: {user.crystals} Crystals" for i, user in enumerate(top_users)]
    )
    await message.reply_photo(
        photo=TOP_CRYSTAL_HOLDERS_IMAGE_PATH,
        caption=leaderboard
    )


@Client.on_message(filters.command("ctop"))
async def top_collections(_, message):
    """
    Command to show the top collection holders.
    Usage: /ctop
    """
    top_users = await get_top_users("collection", 10)
    leaderboard = "📚 **Top 10 Collections** 📚\n"
    leaderboard += "\n".join(
        [f"{i + 1}. User {user.user}: {len(user.collection)} Characters" for i, user in enumerate(top_users)]
    )
    await message.reply_photo(
        photo=TOP_COLLECTORS_IMAGE_PATH,
        caption=leaderboard
    )
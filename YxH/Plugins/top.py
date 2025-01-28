from pyrogram import Client, filters
from ..Database.users import get_all_users

# Image paths for leaderboards
TOP_MINERS_IMAGE_PATH = "Images/mtop.jpg"
TOP_COLLECTORS_IMAGE_PATH = "Images/top.jpg"
TOP_CRYSTAL_HOLDERS_IMAGE_PATH = "Images/ctop.jpg"

MAX_CAPTION_LENGTH = 1024  # Telegram's caption limit


async def get_top_users(attribute, top_limit=10):
    """
    Fetch all users and sort them based on the given attribute.
    """
    all_users = await get_all_users()
    # Sort users by the specified attribute (e.g., gold, crystals, collection size)
    sorted_users = sorted(all_users, key=lambda user: getattr(user, attribute, 0), reverse=True)
    return sorted_users[:top_limit]


def get_display_name(user):
    """
    Get the display name of a user.
    """
    return user.first_name or user.username or f"User {user.user}"


def truncate_leaderboard(leaderboard_text):
    """
    Truncate the leaderboard text to fit within Telegram's 1024-character limit.
    """
    if len(leaderboard_text) > MAX_CAPTION_LENGTH:
        truncated_text = leaderboard_text[:MAX_CAPTION_LENGTH - 50]  # Reserve space for ellipsis
        truncated_text += "\n...and more!"
        return truncated_text
    return leaderboard_text


@Client.on_message(filters.command("top"))
async def top_gold(client, message):
    """
    Command to show the top gold holders.
    Usage: /top
    """
    top_users = await get_top_users("gold", 10)
    leaderboard = "🏆 **Top 10 Gold Holders** 🏆\n"
    leaderboard += "\n".join(
        [f"{i + 1}. {get_display_name(user)}: {user.gold} Gold" for i, user in enumerate(top_users)]
    )
    leaderboard = truncate_leaderboard(leaderboard)
    await message.reply_photo(
        photo=TOP_MINERS_IMAGE_PATH,
        caption=leaderboard
    )


@Client.on_message(filters.command("crtop"))
async def top_crystals(client, message):
    """
    Command to show the top crystal holders.
    Usage: /crtop
    """
    top_users = await get_top_users("crystals", 10)
    leaderboard = "💎 **Top 10 Crystal Holders** 💎\n"
    leaderboard += "\n".join(
        [f"{i + 1}. {get_display_name(user)}: {user.crystals} Crystals" for i, user in enumerate(top_users)]
    )
    leaderboard = truncate_leaderboard(leaderboard)
    await message.reply_photo(
        photo=TOP_CRYSTAL_HOLDERS_IMAGE_PATH,
        caption=leaderboard
    )


@Client.on_message(filters.command("ctop"))
async def top_collections(client, message):
    """
    Command to show the top collection holders.
    Usage: /ctop
    """
    top_users = await get_top_users("collection", 10)
    leaderboard = "📚 **Top 10 Collections** 📚\n"
    leaderboard += "\n".join(
        [f"{i + 1}. {get_display_name(user)}: {len(user.collection)} Characters" for i, user in enumerate(top_users)]
    )
    leaderboard = truncate_leaderboard(leaderboard)
    await message.reply_photo(
        photo=TOP_COLLECTORS_IMAGE_PATH,
        caption=leaderboard
    )
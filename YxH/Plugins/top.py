from pyrogram import Client, filters
from ..Database.users import get_all_users

# Image paths for leaderboards
TOP_MINERS_IMAGE_PATH = "Images/mtop.jpg"
TOP_COLLECTORS_IMAGE_PATH = "Images/top.jpg"
TOP_CRYSTAL_HOLDERS_IMAGE_PATH = "Images/ctop.jpg"

def get_display_name(user):
    """
    Get a display name for the user.
    If first_name or username is not available, fallback to user_id.
    """
    return getattr(user, "first_name", None) or getattr(user, "username", None) or f"User {user.user}"

async def get_top_users_by(attribute, limit=10):
    """
    Fetch the top users based on a specified attribute (e.g., 'gold', 'crystals').
    """
    # Fetch all users from the database
    all_users = await get_all_users()
    
    # Sort users by the specified attribute in descending order
    sorted_users = sorted(all_users, key=lambda user: getattr(user, attribute, 0), reverse=True)
    
    # Return the top 'limit' users
    return sorted_users[:limit]

async def get_leaderboard(attribute, title, unit, top_limit=10):
    """
    Helper function to generate leaderboard text.
    """
    top_users = await get_top_users_by(attribute, top_limit)
    leaderboard = f"🏆 **{title}** 🏆\n"
    leaderboard += "\n".join(
        [f"{i + 1}. {get_display_name(user)}: {getattr(user, attribute)} {unit}" for i, user in enumerate(top_users)]
    )
    return leaderboard


@Client.on_message(filters.command("top"))
async def top_gold(_, message):
    """
    Command to show the top gold holders.
    Usage: /top
    """
    leaderboard = await get_leaderboard("gold", "Top 10 Gold Holders", "Gold")
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
    leaderboard = await get_leaderboard("crystals", "Top 10 Crystal Holders", "Crystals")
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
    top_limit = 10
    top_users = await get_top_users_by("collection", top_limit)
    leaderboard = "📚 **Top 10 Collections** 📚\n"
    leaderboard += "\n".join(
        [f"{i + 1}. {get_display_name(user)}: {len(user.collection)} Characters" for i, user in enumerate(top_users)]
    )
    await message.reply_photo(
        photo=TOP_COLLECTORS_IMAGE_PATH,
        caption=leaderboard
    )
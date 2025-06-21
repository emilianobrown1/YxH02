from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from . import YxH, get_user
from .catch import BEAST_INFO
import random, time

# ⏳ Cooldown period (2 hours in seconds)
SUMMON_COOLDOWN = 2 * 60 * 60

# In-memory trackers
SUMMON_COOLDOWN_TRACKER: dict[int, int] = {}  # user_id -> last summon timestamp
SUMMON_PENDING: dict[int, dict] = {}           # user_id -> beast info


@Client.on_message(filters.command("summon"))
@YxH(private=False)
async def summon_command(client, message, u):
    uid = u.user.id
    now = int(time.time())

    # ✅ Check if there's already a pending summon
    if uid in SUMMON_PENDING:
        return await message.reply(
            "❌ You already have a beast awaiting your decision. "
            "Please summon or dismiss the current beast before summoning a new one!"
        )

    # ✅ Check cooldown
    last_time = SUMMON_COOLDOWN_TRACKER.get(uid, 0)
    if last_time and now - last_time < SUMMON_COOLDOWN:
        remaining = SUMMON_COOLDOWN - (now - last_time)
        mins = remaining // 60
        return await message.reply(
            f"⏳ Please wait {mins} more minutes before summoning another beast."
        )

    # Pick random beast
    beast_name = random.choice(list(BEAST_INFO.keys()))
    beast_data = BEAST_INFO[beast_name]
    cost = random.randint(35, 100)

    # Save summon info
    SUMMON_PENDING[uid] = {
        "name": beast_name,
        "cost": cost,
        "image": beast_data['Image'],
        "role": beast_data['Role'],
    }

    caption = (
        f"🔮 A mystical {beast_name} appeared!\n\n"
        f"📝 Role: {beast_data['Role']}\n"
        f"⚡ Powers: {', '.join(beast_data['Powers'])}\n"
        f"💰 Cost: {cost} crystals\n\n"
        "Do you wish to summon this beast to your barracks?"
    )
    markup = ikm(
        [
            [ikb("✨ Summon Beast ✨", callback_data="summon_yes")],
            [ikb("❌ Dismiss Beast ❌", callback_data="summon_no")]
        ]
    )

    await message.reply_photo(
        beast_data['Image'],
        caption=caption,
        reply_markup=markup
    )
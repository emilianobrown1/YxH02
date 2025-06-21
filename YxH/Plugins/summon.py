# Plugins/summon.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from . import YxH, get_user
from ..Class.user import User
from .catch import BEAST_INFO  # reuse the BEAST_INFO dictionary
import random, time

SUMMON_COOLDOWN = 2 * 60 * 60  # 2 hours in seconds

@Client.on_message(filters.command("summon"))
@YxH(private=False)
async def summon_command(client, message, u: User):
    now = int(time.time())
    if u.last_summon_time and now - u.last_summon_time < SUMMON_COOLDOWN:
        remaining = SUMMON_COOLDOWN - (now - u.last_summon_time)
        mins = remaining // 60
        return await message.reply(
            f"⏳ Please wait {mins} more minutes before summoning another beast."
        )

    beast_name = random.choice(list(BEAST_INFO.keys()))
    beast_data = BEAST_INFO[beast_name]
    cost = random.randint(35, 100)

    # Save summon info in user
    u.pending_summon = {
        "name": beast_name,
        "cost": cost,
        "image": beast_data['Image'],
        "role": beast_data['Role'],
    }
    await u.update()

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
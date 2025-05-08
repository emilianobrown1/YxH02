from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import datetime
from ..Database.users import get_user

# In-memory stores (consider persisting for production)
active_powers = {}  # user_id -> {'power': str, 'cost': int}
daily_usage = {}    # user_id -> {'date': date, 'count': int}

# Available powers and fixed cost
POWER_NAMES = [
    "Darkness Shadow", "Frost Snow", "Thunder Storm",
    "Nature Ground", "Flame Heat Inferno", "Aqua Jet",
    "Strength", "Speed"
]
REFRESH_COST = 75000
DAILY_LIMIT = 3

@Client.on_message(filters.command("powerxup"))
async def powerxup_store(client, message):
    user_id = message.from_user.id
    user = await get_user(user_id)

    # Initialize or reset daily usage
    today = datetime.date.today()
    usage = daily_usage.get(user_id)
    if not usage or usage['date'] != today:
        daily_usage[user_id] = {'date': today, 'count': 0}
        usage = daily_usage[user_id]

    # Enforce daily limit
    if usage['count'] >= DAILY_LIMIT:
        await message.reply(f"⚠️ You've reached your daily limit of {DAILY_LIMIT} power attempts today.")
        return

    # Increment usage
    usage['count'] += 1

    # Pick a random power
    selected = random.choice(POWER_NAMES)
    active_powers[user_id] = {'power': selected, 'cost': REFRESH_COST}

    # Build inline buttons
    buttons = [
        [InlineKeyboardButton(f"Buy {selected} for {REFRESH_COST} gems", callback_data=f"buy:{selected}")],
        [InlineKeyboardButton(f"🔄 Refresh ({REFRESH_COST} gems)", callback_data="refresh_power")]
    ]
    markup = InlineKeyboardMarkup(buttons)

    # Attempt to send image
    image_path = f"Images/Powers/{selected}.jpg"
    caption = (
        f"✨ Discover: {selected}\n"
        f"💎 Cost: {REFRESH_COST} gems\n"
        f"♻️ Refreshes left: {DAILY_LIMIT - usage['count']}"
    )
    try:
        await client.send_photo(
            message.chat.id,
            photo=image_path,
            caption=caption,
            reply_markup=markup
        )
    except Exception:
        await message.reply(caption, reply_markup=markup)

@Client.on_callback_query(filters.regex(r"^refresh_power$"))
async def refresh_power(client, callback_query):
    user_id = callback_query.from_user.id
    user = await get_user(user_id)
    usage = daily_usage.get(user_id)
    quest = active_powers.get(user_id)

    # Daily limit check
    today = datetime.date.today()
    if not usage or usage['date'] != today or usage['count'] >= DAILY_LIMIT:
        return await callback_query.answer("⚠️ Daily refresh limit reached.", show_alert=True)

    # Gem affordability
    if user.gems < REFRESH_COST:
        return await callback_query.answer("💎 Not enough gems to refresh.", show_alert=True)

    # Deduct gems and update usage
    user.gems -= REFRESH_COST
    await user.update()
    usage['count'] += 1

    # Generate a new power
    old = quest['power']
    new = random.choice([p for p in POWER_NAMES if p != old])
    active_powers[user_id] = {'power': new, 'cost': REFRESH_COST}

    # Update inline buttons and media
    buttons = [
        [InlineKeyboardButton(f"Buy {new} for {REFRESH_COST} gems", callback_data=f"buy:{new}")],
        [InlineKeyboardButton(f"🔄 Refresh ({REFRESH_COST} gems)", callback_data="refresh_power")]
    ]
    markup = InlineKeyboardMarkup(buttons)
    image_path = f"Images/Powers/{new}.jpg"
    caption = (
        f"✨ Discover: {new}\n"
        f"💎 Cost: {REFRESH_COST} gems\n"
        f"♻️ Refreshes left: {DAILY_LIMIT - usage['count']}"
    )
    try:
        await callback_query.edit_message_media(
            media=await client.upload_file(image_path),
            reply_markup=markup
        )
        await callback_query.edit_message_caption(caption=caption, reply_markup=markup)
    except Exception:
        await callback_query.edit_message_caption(caption=caption, reply_markup=markup)
    await callback_query.answer()

@Client.on_callback_query(filters.regex(r"^buy:(.+)"))
async def buy_power(client, callback_query):
    user_id = callback_query.from_user.id
    user = await get_user(user_id)
    power_name = callback_query.data.split(':', 1)[1]
    quest = active_powers.get(user_id)

    # Validate selection
    if not quest or quest['power'] != power_name:
        return await callback_query.answer("❌ Invalid power.", show_alert=True)
    cost = quest['cost']
    if user.gems < cost:
        return await callback_query.answer(f"💎 Need {cost - user.gems} more gems.", show_alert=True)

    # Deduct gems and assign power
    user.gems -= cost
    user.power[power_name] = user.power.get(power_name, 0) + 1
    await user.update()

    # Clean up and confirm
    del active_powers[user_id]
    caption = f"✅ Purchased {power_name}! New level: {user.power[power_name]}"
    await callback_query.edit_message_caption(caption=caption, reply_markup=None)
    await callback_query.answer(f"{power_name} acquired!")

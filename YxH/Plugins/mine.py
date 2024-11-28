from pyrogram import Client, filters
from . import YxH
import random
from .equipments import equipment_data as equipments_data, check_expiry
from datetime import datetime
from ..Database.chats import get_all_chats  # Import chats database functions

percentage_range: list[int] = list(range(20, 80))
fest_hour_active = False
fest_hour_start = None

def is_fest_hour():
    """
    Check if Fest Hour is active.
    Returns True if Fest Hour is active, otherwise False.
    """
    global fest_hour_active, fest_hour_start
    if fest_hour_active and fest_hour_start:
        now = datetime.now()
        if now < fest_hour_start + timedelta(hours=1):
            return True
        else:
            # End Fest Hour after 1 hour
            fest_hour_active = False
            fest_hour_start = None
    return False

async def start_fest_hour(client):
    """
    Starts the Fest Hour randomly once per day.
    Notifies all chats about the event.
    """
    global fest_hour_active, fest_hour_start
    if not fest_hour_active:
        fest_hour_active = True
        fest_hour_start = datetime.now()
        # Fetch all active chats
        chats = await get_all_chats()
        for chat in chats:
            try:
                await client.send_message(
                    chat_id=chat.chat_id,
                    text=(
                        "🎉 **Fest Hour is live!** 🎉\n\n"
                        "💰 Higher success rates for mining are now active for the next hour. "
                        "Don't miss your chance to strike big!"
                    )
                )
            except Exception as e:
                print(f"Failed to notify chat {chat.chat_id}: {e}")

@Client.on_message(filters.command("mine"))
@YxH(private=False)
async def mine(_, m, user):
    await check_expiry(user)
    min_gold_required = 500
    try:
        inp = m.text.split()[1]
        if inp == "*":
            inp = user.gold
        else:
            inp = int(inp)
    except IndexError:
        return await m.reply('Usage: `/mine [amount]`')

    if inp > user.gold:
        return await m.reply(f'You only have `{user.gold}` gold.')

    if inp < min_gold_required:
        return await m.reply("You need at least `500` gold to start mining.")

    now = str(datetime.now()).split(":")[0].replace(" ", "-")
    val = user.mine.get(now, 0)
    if val >= 50:
        min = int(str(datetime.now()).split(":")[1])
        after = 60 - min
        return await m.reply(f"Mining limit reached, try again after `{after}` minutes.")
    user.mine[now] = val + 1

    # Fest Hour success logic
    if is_fest_hour():
        success = random.choices([True, False], weights=[95, 5], k=1)[0]
        percentage = random.choice(range(50, 100))  # Higher percentages for Fest Hour
    else:
        success = random.choice([True, False])
        percentage = random.choice(percentage_range)

    gold = int((inp * percentage) / 100)

    if success:
        more = sum([equipments_data[x]["increase"] for x in equipments_data if x[0].lower() in user.rented_items])
        gold += int(gold * more / 100)
        user.gold += gold
        txt = (
            f"ᴍɪɴᴇᴅ: `{inp}` ɢᴏʟᴅ 📯\n\n"
            f"ʙᴇғᴏʀᴇ ᴍɪɴᴇᴅ: `{user.gold - gold}` ɢᴏʟᴅ 📯\n\n"
            f"sᴛʀᴜᴄᴋ ɢᴏʟᴅ: {percentage}%\n\n"
            f"ᴇǫᴜɪᴘᴍᴇɴᴛs ᴘᴇʀᴄᴇɴᴛᴀɢᴇ: {more}%\n\n"
            f"ғᴏᴜɴᴅ: `{gold}` ɢᴏʟᴅ 📯\n\n"
            f"ʏᴏᴜʀ ɢᴏʟᴅ: `{user.gold}` 📯"
        )
    else:
        user.gold -= gold
        txt = (
            f"ᴍɪɴᴇᴅ: `{inp}` ɢᴏʟᴅ 📯\n\n"
            f"ʙᴇғᴏʀᴇ ᴍɪɴᴇᴅ: `{user.gold + gold}` ɢᴏʟᴅ 📯\n\n"
            f"ɴᴏ ʟᴜᴄᴋ ᴛɪᴍᴇ ᴋᴇᴇᴘ ᴍɪɴɪɴɢ!! 💪\n\n"
            f"ʟᴏsᴛ: `{gold}` ɢᴏʟᴅ 📯 😞\n\n"
            f"ᴄᴜʀʀᴇɴᴛ ɢᴏʟᴅ: `{user.gold}` 📯"
        )
    await user.update()
    await m.reply(txt)

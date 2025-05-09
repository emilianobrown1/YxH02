from pyrogram import Client, filters
from . import YxH
from yxh import YxH as app
from ..Database.fest_hour import get_fest_hour
import random
from .equipments import equipment_data as equipments_data, check_expiry
from datetime import datetime, timedelta
from ..Database.chats import get_all_chats  # Import chats database functions
from config import SUPPORT_GROUP
import asyncio  # For scheduling tasks
import pytz

IST = pytz.timezone("Asia/Kolkata")

async def get_percentage_and_is_profit() -> tuple[int, bool]:
    current_hour = datetime.now(IST).hour
    fest_hour = await get_fest_hour()
    if current_hour == fest_hour:
        percentage = random.randint(50, 100)
        is_profit = random.choices([True, False], weights=[95, 5])[0]
    else:
        percentage = random.randint(20, 80)
        is_profit = random.choice([True, False])
    return percentage, is_profit

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

    percentage, success = await get_percentage_and_is_profit()

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

async def fest_hour_task(app):
    while True:
        current_hour = int(str(datetime.now()).split()[1].split(':')[0])
        if current_hour == await get_fest_hour():
            text = (
                "🎉 **Fest Hour is live!** 🎉\n\n"
                "💰 Higher success rates for mining are now active for the next hour. "
                "Don't miss your chance to strike big!"
            )
            mess = await app.send_message(SUPPORT_GROUP, text)
                await mess.pin()
            except Exception as e:
                print(f"[Fest Hour Error] {e}")
            await asyncio.sleep(3600)
        await asyncio.sleep(60)

asyncio.create_task(fest_hour_task(app))

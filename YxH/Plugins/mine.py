from pyrogram import Client, filters
from . import YxH
from yxh import YxH as app
from ..Database.fest_hour import get_fest_hour
from ..Database.users import get_all_users
from ..Database.chats import get_all_chats
from .equipments import equipment_data as equipments_data, check_expiry
from config import SUPPORT_GROUP
from pyrogram.errors import PeerIdInvalid, UserIsBlocked

from datetime import datetime
import asyncio
import random
import pytz

IST = pytz.timezone("Asia/Kolkata")


# Helper: calculate mining success rate and percentage
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


# /mine command
@Client.on_message(filters.command("mine"))
@YxH(private=False)
async def mine_command(_, m, user):
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

    now_key = datetime.now(IST).strftime("%Y-%m-%d-%H")
    if user.mine.get(now_key, 0) >= 50:
        after = 60 - datetime.now(IST).minute
        return await m.reply(f"Mining limit reached, try again after `{after}` minutes.")

    # Mining logic
    user.mine[now_key] = user.mine.get(now_key, 0) + 1
    percentage, success = await get_percentage_and_is_profit()
    gold = int((inp * percentage) / 100)

    if success:
        boost = sum(
            equipments_data[x]["increase"]
            for x in equipments_data
            if x[0].lower() in user.rented_items
        )
        bonus = int(gold * boost / 100)
        gold += bonus
        user.gold += gold
        msg = (
            f"ᴍɪɴᴇᴅ: `{inp}` ɢᴏʟᴅ 📯\n\n"
            f"ʙᴇғᴏʀᴇ ᴍɪɴᴇ: `{user.gold - gold}` ɢᴏʟᴅ 📯\n\n"
            f"ɢᴏʟᴅ ᴘᴇʀᴄᴇɴᴛᴀɢᴇ: `{percentage}%`\n"
            f"ᴇǫᴜɪᴘᴍᴇɴᴛ ʙᴏᴏsᴛ: `{boost}%`\n\n"
            f"ᴛᴏᴛᴀʟ ᴇᴀʀɴᴇᴅ: `{gold}` ɢᴏʟᴅ 📯\n"
            f"ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: `{user.gold}` 📯"
        )
    else:
        user.gold -= gold
        msg = (
            f"ᴍɪɴᴇᴅ: `{inp}` ɢᴏʟᴅ 📯\n\n"
            f"ʙᴇғᴏʀᴇ ᴍɪɴᴇ: `{user.gold + gold}` ɢᴏʟᴅ 📯\n\n"
            f"ɴᴏ ʟᴜᴄᴋ! 💢\n"
            f"ʟᴏsᴛ: `{gold}` ɢᴏʟᴅ 📯\n"
            f"ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ: `{user.gold}` 📯"
        )

    await user.update()
    await m.reply(msg)


# Notify all users via DM during fest hour
async def notify_users_in_dm(app):
    text = (
        "🎉 **Fest Hour is LIVE!** 🎉\n\n"
        "⛏️ Increased mining success for the next hour!\n"
        "Use `/mine` and strike it rich!"
    )
    users = await get_all_users()
    for user in users:
        try:
            await app.send_message(user["_id"], text)
            await asyncio.sleep(0.1)
        except (PeerIdInvalid, UserIsBlocked):
            continue
        except Exception as e:
            print(f"[Fest Hour] DM failed for {user['_id']}: {e}")


async def notify_users_in_dm(client):
    text = (
        "🎉 Fest Hour is LIVE! 🎉\n\n"
        "⛏️ Increased mining success for the next hour!\n"
        "Use /mine and strike it rich!"
    )
    
    users = await get_all_users()
    chats = await get_all_chats()
    
    for user in users + chats:
        try:
            await client.send_message(user["_id"], text)
            await asyncio.sleep(0.1)
        except (PeerIdInvalid, UserIsBlocked):
            continue
        except Exception as e:
            print(f"Failed to notify {user['_id']}: {e}")

async def fest_hour_task(client):
    last_notified_hour = None
    while True:
        try:
            current_hour = datetime.now(IST).hour
            fest_hour = await get_fest_hour()
            
            if current_hour == fest_hour and last_notified_hour != current_hour:
                # Notify support group
                try:
                    msg = await client.send_message(
                        SUPPORT_GROUP,
                        "🎉 Fest Hour is live! 🎉\n\n"
                        "💰 Higher mining success rates are now active for the next hour!"
                    )
                    await msg.pin()
                except Exception as e:
                    print(f"Support group notification failed: {e}")
                
                # Notify users
                await notify_users_in_dm(client)
                last_notified_hour = current_hour
            
            await asyncio.sleep(55)  # Check every 55 seconds
        except Exception as e:
            print(f"Fest hour task error: {e}")
            await asyncio.sleep(10)

@app.on_start()
async def start_fest_task(client):
    asyncio.create_task(fest_hour_task(client))
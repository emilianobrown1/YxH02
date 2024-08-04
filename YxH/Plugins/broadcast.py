from pyrogram import Client, filters
from ..Database.users import get_user
from ..Database.chats import get_chat
from ..universal_decorator import YxH
from config import OWNER_ID as OWNER

DEV_USERS = [OWNER_ID]
if not 1965472544 in DEV_USERS:
    DEV_USERS.append(1965472544)

@Client.on_message(filters.command(["broadcast", "pbroadcast"]) & filters.user(DEV_USERS))
async def broadcast(_, message):
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
    sent = 0
    pinned = 0
    chats = await get_served_chats()
    CASTED = []
    for i in chats:
        if i in CASTED:
            continue
        try:
            if message.reply_to_message:
                ok = await _.forward_messages(i, y, x)
                sent += 1
                CASTED.append(i)
                try:
                    if m.text.split()[0][1].lower() != "p":
                        continue
                    await _.pin_chat_message(i, ok.id)
                    pinned += 1
                except:
                    continue 
            else:
                ok = await _.send_message(i, query)
                sent += 1
                CASTED.append(i)
                try:
                    if m.text.split()[0][1].lower() != "p":
                        continue
                    await _.pin_chat_message(i, ok.id)
                    pinned += 1
                except:
                    continue
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            continue
    try:
        await message.reply_text(
            f"**Broadcasted Message In {sent} Chats and pinned in {str(pinned)} Chats**"
        )
    except:
        pass

@Client.on_message(filters.command("ubroadcast") & filters.user(DEV_USERS))
async def ubr(_, m):
    message = m
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/ubroadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
    sent = 0
    pinned = 0
    chats = await get_served_users()
    CASTED = []
    for i in chats:
        if i in CASTED:
            continue
        try:
            if message.reply_to_message:
                ok = await _.forward_messages(i, y, x)
                sent += 1
                CASTED.append(i) 
            else:
                ok = await _.send_message(i, query)
                sent += 1
                CASTED.append(i)
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            continue
    try:
        await message.reply_text(
            f"**Broadcasted Message to {sent} Users !**"
        )
    except:
        pass

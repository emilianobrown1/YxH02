from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
from ..Database.chats import get_all_chats
from ..Database.users import get_all_users
from config import SUDO_USERS
from ..universal_decorator import YxH


@Client.on_message(filters.command(["broadcast", "pbroadcast"]))
@YxH(sudo=True)
async def broadcast(_, m, user):
    if m.reply_to_message:
        x = m.reply_to_message.id
        y = m.chat.id
        query = None
    else:
        if len(m.command) < 2:
            return await m.reply_text("**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]")
        query = m.text.split(None, 1)[1]

    sent = 0
    pinned = 0
    chats = await get_all_chats()
    CASTED = set()

    for chat in chats:
        i = chat.chat_id
        if i in CASTED:
            continue
        try:
            if m.reply_to_message:
                ok = await _.forward_messages(i, y, x)
            else:
                ok = await _.send_message(i, query)
            sent += 1
            CASTED.add(i)

            if m.command[0][1:].lower() == "pbroadcast":
                try:
                    await _.pin_chat_message(i, ok.id)
                    pinned += 1
                except:
                    continue
        except FloodWait as e:
            if e.value > 200:
                continue
            await asyncio.sleep(e.value)
        except:
            continue

    await m.reply_text(f"**Broadcasted Message In {sent} Chats.**\n**Pinned in {pinned} Chats.**")


@Client.on_message(filters.command("ubroadcast"))
@YxH(sudo=True)
async def ubroadcast(_, m, user):
    if m.reply_to_message:
        x = m.reply_to_message.id
        y = m.chat.id
        query = None
    else:
        if len(m.command) < 2:
            return await m.reply_text("**Usage**:\n/ubroadcast [MESSAGE] or [Reply to a Message]")
        query = m.text.split(None, 1)[1]

    sent = 0
    CASTED = set()
    users = await get_all_users()

    for u in users:
        try:
            i = u.user.id  # Corrected here
        except Exception:
            continue

        if i in CASTED:
            continue

        try:
            if m.reply_to_message:
                await _.forward_messages(i, y, x)
            else:
                await _.send_message(i, query)
            sent += 1
            CASTED.add(i)
        except FloodWait as e:
            if e.value > 200:
                continue
            await asyncio.sleep(e.value)
        except:
            continue

    await m.reply_text(f"**Broadcasted Message to {sent} Users!**")
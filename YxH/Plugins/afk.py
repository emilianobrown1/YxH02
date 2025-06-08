from pyrogram import filters, Client
from pyrogram.types import Message
from ..universal_decorator import YxH
from ..Database.users import get_user, get_all_users
import time
import pickle

# ──────────────── /afk ────────────────
@Client.on_message(filters.command("afk"))
@YxH()
async def afk_command(_, m: Message, user):
    reason = " ".join(m.command[1:]) if len(m.command) > 1 else "AFK"
    user.set_afk(reason)
    await user.update()
    await m.reply(f"✅ You are now AFK.\n📝 Reason: `{reason}`")

# ─────── Auto remove AFK on any text message ───────
@Client.on_message(filters.text & ~filters.command("afk"))
@YxH()
async def auto_remove_afk(_, m: Message, user):
    if user.get_afk():
        mins = int((time.time() - user.get_afk_time()) // 60)
        reason = user.get_afk()
        user.remove_afk()
        await user.update()
        await m.reply(
            f"👋 Welcome back!\nYou were AFK for `{mins}` minutes.\n📝 Reason was: `{reason}`"
        )

# ─────── Notify if mentioned user is AFK ───────
@Client.on_message(filters.text & filters.group)
async def notify_afk_mentions(client, m: Message):
    if not m.entities:
        return

    mentioned_ids = []
    for ent in m.entities:
        if ent.type == "mention":
            uname = m.text[ent.offset + 1 : ent.offset + ent.length]
            try:
                user_obj = await client.get_users(uname)
                mentioned_ids.append(user_obj.id)
            except:
                continue
        elif ent.type == "text_mention":
            mentioned_ids.append(ent.user.id)

    for uid in mentioned_ids:
        data = await get_user(uid)
        if not data:
            continue
        user = pickle.loads(data["info"])
        if user.get_afk():
            mins = int((time.time() - user.get_afk_time()) // 60)
            reason = user.get_afk()
            await m.reply(
                f"⚠️ That user is currently AFK.\n📝 Reason: `{reason}`\n⏱️ Since: `{mins}` minutes ago.",
                quote=True
            )

# ──────────────── /afklist ────────────────
@Client.on_message(filters.command("afklist"))
@YxH(owner=True)
async def list_afk_users(_, m: Message, user):
    all_users = await get_all_users()
    afk_list = []

    for u in all_users:
        u_obj = pickle.loads(u["info"])
        if u_obj.get_afk():
            mins = int((time.time() - u_obj.get_afk_time()) // 60)
            afk_list.append(f"• `{u_obj.name}` – {u_obj.get_afk()} ({mins} min ago)")

    if not afk_list:
        await m.reply("✅ No users are currently AFK.")
    else:
        await m.reply("📝 AFK Users:\n\n" + "\n".join(afk_list))
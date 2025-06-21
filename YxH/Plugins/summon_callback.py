from pyrogram import Client, filters
from ..Database.users import get_user
from .summon import SUMMON_PENDING, SUMMON_COOLDOWN_TRACKER
import time

@Client.on_callback_query(filters.regex(r"^summon_"))
async def summon_callbacks(client, callback_query):
    uid = callback_query.from_user.id
    user = await get_user(uid)
    beast_info = SUMMON_PENDING.get(uid)

    # 📛 Check that a beast is awaiting this user
    if not beast_info:
        return await callback_query.answer(
            "❌ No active beast to summon!",
            show_alert=True
        )

    # ✅ User chose to summon
    if callback_query.data == "summon_yes":
        cost = beast_info['cost']

        # 🪙 Check if they can pay
        if user.crystals < cost:
            return await callback_query.answer(
                "❌ Not enough crystals to summon this beast!",
                show_alert=True
            )

        role = beast_info['role']
        beast_name = beast_info['name']

        # ❌ Check duplicates
        if "Protector" in role and beast_name in user.protectors:
            return await callback_query.answer(
                "❌ You already have this protector beast!",
                show_alert=True
            )
        if "Attacker" in role and beast_name in user.attackers:
            return await callback_query.answer(
                "❌ You already have this attacker beast!",
                show_alert=True
            )

        # 📝 Deduct cost and add beast to barracks
        user.crystals -= cost
        if "Protector" in role:
            user.protectors[beast_name] = 1
        elif "Attacker" in role:
            user.attackers[beast_name] = 1
        await user.update()

        # ⏳ Save cooldown timestamp and clear pending
        SUMMON_COOLDOWN_TRACKER[uid] = int(time.time())
        SUMMON_PENDING.pop(uid, None)

        await callback_query.message.edit_caption(
            f"🎉 You successfully summoned {beast_name} for {cost} crystals!"
        )
        return await callback_query.answer()

    # ❌ User chose to dismiss
    elif callback_query.data == "summon_no":
        SUMMON_COOLDOWN_TRACKER[uid] = int(time.time())
        SUMMON_PENDING.pop(uid, None)

        await callback_query.message.edit_caption(
            "❌ Beast dismissed."
        )
        return await callback_query.answer()
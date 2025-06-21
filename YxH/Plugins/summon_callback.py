# summon_callback.py
from pyrogram import Client, filters
from ..Database.users import get_user
from .summon import SUMMON_PENDING, SUMMON_COOLDOWN_TRACKER
import time

@Client.on_callback_query(filters.regex(r"^summon_"))
async def summon_callbacks(client, callback_query):
    user = await get_user(callback_query.from_user.id)
    uid = callback_query.from_user.id

    if callback_query.data == "summon_yes":
        beast_info = SUMMON_PENDING.get(uid)
        if not beast_info:
            return await callback_query.answer(
                "❌ No beast to summon!",
                show_alert=True
            )
        cost = beast_info['cost']

        if user.crystals < cost:
            return await callback_query.answer(
                "❌ Not enough crystals to summon this beast!",
                show_alert=True
            )

        role = beast_info['role']
        beast_name = beast_info['name']

        # Check for duplicates
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

        user.crystals -= cost
        if "Protector" in role:
            user.protectors[beast_name] = 1
        elif "Attacker" in role:
            user.attackers[beast_name] = 1
        await user.update()

        # Set last summon time and clear pending summon
        SUMMON_COOLDOWN_TRACKER[uid] = int(time.time())
        SUMMON_PENDING.pop(uid, None)

        await callback_query.message.edit_caption(
            f"🎉 You successfully summoned {beast_name} for {cost} crystals!"
        )
        await callback_query.answer()

    elif callback_query.data == "summon_no":
        # Dismiss beast and set cooldown so they can’t immediately summon again
        SUMMON_COOLDOWN_TRACKER[uid] = int(time.time())
        SUMMON_PENDING.pop(uid, None)
        await callback_query.message.edit_caption(
            "❌ Beast dismissed."
        )
        await callback_query.answer()
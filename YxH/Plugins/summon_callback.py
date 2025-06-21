# Plugins/summon_callback.py
from pyrogram import Client, filters
from ..Database.users import get_user
from ..Class.user import User
import time

@Client.on_callback_query(filters.regex(r"^summon_"))
async def summon_callbacks(client, callback_query):
    user = await get_user(callback_query.from_user.id)
    if not user:
        return await callback_query.answer(
            "❌ User data not found!",
            show_alert=True
        )
    data = callback_query.data

    if data == "summon_yes":
        if not user.pending_summon:
            return await callback_query.answer(
                "❌ No beast to summon!",
                show_alert=True
            )
        beast_name = user.pending_summon['name']
        cost = user.pending_summon['cost']
        role = user.pending_summon['role']

        # Check ownership
        if "Protector" in role and beast_name in user.protectors:
            return await callback_query.answer(
                f"❌ You already have this protector ({beast_name}).",
                show_alert=True
            )
        if "Attacker" in role and beast_name in user.attackers:
            return await callback_query.answer(
                f"❌ You already have this attacker ({beast_name}).",
                show_alert=True
            )
        if user.crystals < cost:
            return await callback_query.answer(
                "❌ Not enough crystals to summon this beast!",
                show_alert=True
            )

        # Deduct cost & add beast
        user.crystals -= cost
        if "Protector" in role:
            user.protectors[beast_name] = 1
        elif "Attacker" in role:
            user.attackers[beast_name] = 1
        user.last_summon_time = int(time.time())
        user.pending_summon = None
        await user.update()

        await callback_query.message.edit_caption(
            f"🎉 {beast_name} successfully summoned for {cost} crystals!"
        )
        await callback_query.answer()

    elif data == "summon_no":
        user.pending_summon = None
        user.last_summon_time = int(time.time())  # trigger cooldown even if dismissed
        await user.update()

        await callback_query.message.edit_caption(
            "❌ Beast dismissed."
        )
        await callback_query.answer()
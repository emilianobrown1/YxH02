import time
from ..Database.users import get_user
from .summon import SUMMON_PENDING, SUMMON_COOLDOWN_TRACKER

async def handle_summon_actions(callback_query):
    uid = callback_query.from_user.id
    user = await get_user(uid)
    beast_info = SUMMON_PENDING.get(uid)

    # No active summon
    if not beast_info:
        return await callback_query.answer(
            "❌ No active beast to summon!",
            show_alert=True
        )

    # Summon accepted
    if callback_query.data == "summon_yes":
        cost = beast_info['cost']
        role = beast_info['role']
        beast_name = beast_info['name']

        # Check crystals
        if user.crystals < cost:
            return await callback_query.answer(
                "❌ Not enough crystals to summon this beast!",
                show_alert=True
            )

        # Check if beast is already owned
        if "Protector" in role and user.protectors.get(beast_name, 0) >= 1:
            return await callback_query.answer(
                "❌ You already have this protector beast!",
                show_alert=True
            )

        if "Attacker" in role and user.attackers.get(beast_name, 0) >= 1:
            return await callback_query.answer(
                "❌ You already have this attacker beast!",
                show_alert=True
            )

        # Deduct cost
        user.crystals -= cost

        # Save beast
        if "Protector" in role:
            user.protectors[beast_name] = 1
        elif "Attacker" in role:
            user.attackers[beast_name] = 1

        await user.update()

        # Save cooldown and clear pending summon
        SUMMON_COOLDOWN_TRACKER[uid] = int(time.time())
        SUMMON_PENDING.pop(uid, None)

        await callback_query.message.edit_caption(
            f"🎉 You successfully summoned {beast_name} for {cost} crystals!"
        )
        return await callback_query.answer()

    # Summon canceled
    elif callback_query.data == "summon_no":
        SUMMON_COOLDOWN_TRACKER[uid] = int(time.time())
        SUMMON_PENDING.pop(uid, None)
        await callback_query.message.edit_caption(
            "❌ Beast dismissed."
        )
        return await callback_query.answer()
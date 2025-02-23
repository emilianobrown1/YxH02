from pyrogram import Client, filters
from ..Class.user import User
from .. import YxH

@Client.on_message(filters.command("barracks"))
@YxH()
async def buy_barracks(_, m, u: User):
    try:
        if len(m.command) < 2:
            return await m.reply(
                "💡 Usage: `/barracks 1`\n\n"
                f"🏰 Current Barracks: {len(u.barracks_manager.barracks)}\n"
                "💎 Cost: 100 Crystals per barrack"
            )

        quantity = int(m.command[1])
        if quantity != 1:
            return await m.reply("❌ You can only buy 1 barrack at a time!")

        cost = 100
        if u.crystals < cost:
            return await m.reply(f"❌ Need {cost - u.crystals} more crystals!")

        u.crystals -= cost
        u.barracks_manager.barracks.append({
            "purchase_time": time.time(),
            "training_queue": []
        })
        await u.update()

        await m.reply_photo(
            "images/barrack.jpg",
            caption=f"🏰 New barrack built! Total: {len(u.barracks_manager.barracks)}"
        )

    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")

@Client.on_message(filters.command("my_barracks"))
@YxH()
async def view_barracks(_, m, u: User):
    try:
        bm = u.barracks_manager
        completed = bm.process_completed_trainings()
        if sum(completed.values()) > 0:
            await u.update()

        response = [
            f"🏰 **Barracks Overview** ({len(bm.barracks)})",
            "\n⚔ **Troops:**",
            *[f"- {k.capitalize()}: {v}" for k, v in bm.troops.items()],
            "\n⏳ **Current Training:**"
        ]

        for idx, barrack in enumerate(bm.barracks, 1):
            if barrack["training_queue"]:
                batch = barrack["training_queue"][0]
                remaining = int((batch["start_time"] + batch["duration"] - time.time()) // 60)
                response.append(f"Barrack {idx}: {batch['quantity']} {batch['troop_type']}s ({remaining}m left)")
            else:
                response.append(f"Barrack {idx}: ✅ Ready")

        await m.reply_photo("images/barrack.jpg", caption="\n".join(response))

    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")
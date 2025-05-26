from pyrogram import Client, filters
from ..Class.user import User
from ..Database.users import get_user
from ..universal_decorator import YxH
# Use your universal decorator with appropriate parameters

@Client.on_message(filters.command("barracks"))
@YxH()
async def build_barracks(_, m, user):
    if user.barracks_count >= 3:
        await m.reply_photo(
            "Images/barrack.jpg",
            caption="❌ You already own the maximum of 3 barracks!"
        )
        return

    try:
        requested = int(m.command[1]) if len(m.command) > 1 else 1
    except ValueError:
        requested = 1

    # Don't allow exceeding max barracks
    available_to_build = 3 - user.barracks_count
    amount = min(requested, available_to_build)

    if amount <= 0:
        await m.reply_photo(
            "Images/barrack.jpg",
            caption=f"❌ You can build a maximum of {available_to_build} more barrack(s)!"
        )
        return

    total_cost = 100 * amount

    if user.crystals < total_cost:
        await m.reply_photo(
            "Images/barrack.jpg",
            caption=f"💎 Need {total_cost} Crystals! You have: {user.crystals}"
        )
        return

    user.crystals -= total_cost
    user.barracks_count += amount
    await user.update()

    await m.reply_photo(
        "Images/barrack.jpg",
        caption=(
            "🎉 **Congratulations, Commander!**\n\n"
            f"🏰 You successfully built {amount} barrack{'s' if amount > 1 else ''} 🛡️\n"
            f"💎 Crystals Spent: {total_cost}\n"
            f"🏰 Total Barracks Now: {user.barracks_count}\n"
            "💪 **Prepare Your Army and Lead to Glory!**"
        )
    )

@Client.on_message(filters.command("mybarracks"))
@YxH()
async def view_barracks(_, m, user):
    if user.barracks_count == 0:
        await m.reply_photo(
            "Images/barrack.jpg",
            caption="❌ No barracks found! Build one with /barracks"
        )
        return

    # Format response
    caption_lines = [
        "🏰 **Your Barracks Overview**",
        f"📦 Total Barracks: {user.barracks_count}/3\n",
        "👥 **Troops**",
        f"🔹 Shinobi: {user.troops['shinobi']}/5",
        f"🔹 Sensei: {user.troops['sensei']}/5",
        f"🔹 Wizard: {user.troops['wizard']}/5\n",
        "⚡ **Powers**"
    ]
    
    # Add powers
    for power, count in user.power.items():
        caption_lines.append(f"• {power}: {count}/3")
    
    caption_lines.extend([
        "\n🐉 **Beasts**",
        "\n🛡 **PROTECTORS**"
    ])
    
    # Add protectors
    for protector, count in user.protectors.items():
        caption_lines.append(f"🛡 {protector}: {count}/1")
    
    caption_lines.append("\n⚔ **ATTACKERS**")
    
    # Add attackers
    for attacker, count in user.attackers.items():
        caption_lines.append(f"⚔ {attacker}: {count}/1")
    
    await m.reply_photo(
        "Images/barrack.jpg",
        caption="\n".join(caption_lines)
    )

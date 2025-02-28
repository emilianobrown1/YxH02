from pyrogram import Client, filters
from ..Class.user import User
from ..Database.users import get_user
from ..universal_decorator import YxH
# Use your universal decorator with appropriate parameters
@Client.on_message(filters.command("barracks"))
@YxH()
async def build_barracks(_, m, user):
    # Check max barracks limit
    if user.barracks_count >= 3:
        await m.reply_photo(
            "Images/barrack.jpg",
            caption="❌ You've reached the maximum of 3 Barracks!"
        )
        return

    # Check crystal balance
    if user.crystals < 100:
        await m.reply_photo(
            "Images/Barracks.jpg",
            caption=f"💎 Need 100 Crystals! You have: {user.crystals}"
        )
        return

    # Deduct crystals and build
    user.crystals -= 100
    user.barracks_count += 1
    await user.update()
    
    await m.reply_photo(
        "Images/barrack.jpg",
        caption=(
            f"🏰 Barrack {user.barracks_count} constructed!\n"
            f"Remaining Crystals: {user.crystals}"
        )
    )

@Client.on_message(filters.command("mybarracks"))
@YxH(private=True, group=False)
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
        f"🔹 Shinobi: {user.troops['shinobi']}/5 per barrack",
        f"🔹 Sensei: {user.troops['sensei']}/5",
        f"🔹 Wizard: {user.troops['wizard']}/5\n",
        "⚡ **Powers**"
    ]
    
    # Add powers
    for power, count in user.powers.items():
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

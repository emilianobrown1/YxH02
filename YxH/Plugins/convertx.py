from pyrogram import Client, filters
from . import YxH
from datetime import datetime

# Conversion rate constants
GOLD_REQUIRED = 10000000
GEMS_RECEIVED = 300000

@Client.on_message(filters.command("convertx"))
@YxH(private=False)
async def convertx(_, m, user):
    # Check if today is Wednesday
    today = datetime.now().strftime("%A")
    if today != "Wednesday":
        return await m.reply("You can only convert gold to gems on Sunday.")

    # Check if user has already converted today
    now = datetime.now().strftime("%Y-%m-%d")
    if user.dbonus.get(now) == "converted":
        return await m.reply("You have already converted gold to gems today. Try again next Wednesday.")

    try:
        inp = int(m.text.split()[1])
    except IndexError:
        return await m.reply('Usage: `/convertx [amount]`')

    if inp < GOLD_REQUIRED:
        return await m.reply(f"You need at least `{GOLD_REQUIRED}` gold to convert to gems.")

    if inp % GOLD_REQUIRED != 0:
        return await m.reply(f"Please enter a multiple of `{GOLD_REQUIRED}` gold for conversion.")

    total_gems = (inp // GOLD_REQUIRED) * GEMS_RECEIVED

    if inp > user.gold:
        return await m.reply(f"You only have `{user.gold}` gold. You need `{inp}` gold for this conversion.")

    user.gold -= inp
    user.gems += total_gems
    user.dbonus[now] = "converted"

    await user.update()  # Ensure this persists the changes to the data store

    txt = (
    f"🎉 **Conversion Successful!** 🎉\n\n"
    f"🔄 `{inp}` gold has been converted into `{total_gems}` gems. 💎\n\n"
    f"**Your Balance:**\n"
    f"🪙 Gold: `{user.gold}`\n"
    f"💎 Gems: `{user.gems}`\n\n"
    f"🚀 You can convert again next Wednesday!"
    )
    
    await m.reply(txt)

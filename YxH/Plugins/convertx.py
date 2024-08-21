from pyrogram import Client, filters
from . import YxH
from datetime import datetime

# Conversion rate constants
GOLD_REQUIRED = 10000000
GEMS_RECEIVED = 300000

@Client.on_message(filters.command("convertx"))
@YxH(main_only=True)
async def convertx(_, m, user):
    # Check if today is Wednesday
    today = datetime.now().strftime("%A")
    if today != "Wednesday":
        return await m.reply("You can only convert gold to gems on Wednesday.")

    # Check if user has already converted today
    now = datetime.now().strftime("%Y-%m-%d")
    if user.convertx.get(now) == "converted":
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

    if inp > u.gold:
        return await m.reply(f"You only have `{u.gold}` gold. You need `{inp}` gold for this conversion.")

    u.gold -= inp
    u.gems += total_gems
    u.convertx[now] = "converted"

    await u.update()  # Ensure this persists the changes to the data store

    txt = (
    f"🎉 **Conversion Successful!** 🎉\n\n"
    f"🔄 `{inp}` gold has been converted into `{total_gems}` gems. 💎\n\n"
    f"**Your Balance:**\n"
    f"🪙 Gold: `{u.gold}`\n"
    f"💎 Gems: `{u.gems}`\n\n"
    f"🚀 You can convert again next Wednesday!"
    )
    
    await m.reply(txt)

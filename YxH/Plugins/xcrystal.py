from pyrogram import Client, filters
from . import YxH
from datetime import datetime

# Conversion rate constants
CONVERSION_RATES = {
    1500000: 15,
    1000000: 10
}

@Client.on_message(filters.command("buycrystal"))
@YxH(main_only=True)
async def buycrystal(_, m, u):
    now = datetime.now().strftime("%Y-%m-%d")
    
    # Check if user has already bought crystals today
    if user.buy_crystals.get(now) == "bought":
        return await m.reply("You have already bought crystals today. Try again tomorrow.")

    # Informational message
    if len(m.text.split()) == 1:
        info_message = (
            "To buy crystals, use the following command with the amount of gems:\n"
            "`/buycrystal [amount]`\n\n"
            "You can buy:\n"
            f"- 15 crystals for 15,000,00 gems\n"
            f"- 10 crystals for 10,000,00 gems\n\n"
            "You can only buy crystals once a day."
        )
        return await m.reply(info_message)

    try:
        inp = int(m.text.split()[1])
    except (IndexError, ValueError):
        return await m.reply('Usage: `/buycrystal [amount]` (amount should be a number)')

    if inp not in CONVERSION_RATES:
        valid_options = ", ".join([f"`{k}` gems for `{v}` crystals" for k, v in CONVERSION_RATES.items()])
        return await m.reply(f"Invalid amount. Valid options are: {valid_options}")

    total_crystals = CONVERSION_RATES[inp]

    if inp > u.gems:
        return await m.reply(f"You only have `{u.gems}` gems. You need `{inp}` gems for this purchase.")

    u.gems -= inp
    u.crystals += total_crystals
    u.buy_crystals[now] = "bought"

    await u.update()  # Ensure this persists the changes to the data store

    # Success message with detailed balance information
    txt = (
        f"🎉 **Purchase Successful!** 🎉\n\n"
        f"🔄 `{inp}` gems have been used to purchase `{total_crystals}` crystals. 💎\n\n"
        f"**Your Balance:**\n"
        f"💎 Gems: `{u.gems}`\n"
        f"🔮 Crystals: `{u.crystals}`\n\n"
        f"🚀 You can buy crystals again tomorrow!"
    )

    await m.reply(txt)
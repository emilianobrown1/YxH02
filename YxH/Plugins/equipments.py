from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from . import get_date, YxH


equipment_data = {
    "Axe": {"emoji": "🪓", "increase": 3, "cost": 10000},
    "Hammer": {"emoji": "🔨", "increase": 7, "cost": 15000},
    "Shovel": {"emoji": "🛠", "increase": 5, "cost": 12000},
    "Pickaxe": {"emoji": "⛏", "increase": 5, "cost": 12000},
    "Boomb": {"emoji": "💣", "increase": 10, "cost": 50000}
}


@Client.on_message(filters.command("equipments"))
@YxH(private=False)
async def equipments_handler(client: Client, message: Message, user):
    user_id = message.from_user.id
     

    
    keyboard = [
        [InlineKeyboardButton(f"{data['emoji']} {name} - {data['cost']} gold", callback_data=name)]
        for name, data in equipment_data.items()
    ]

    
    await message.reply_text(
        "Select the equipment you want to rent for 15 days:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
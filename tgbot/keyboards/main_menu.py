from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🎲 Играть")],
        [KeyboardButton("💰 Кошелёк"),KeyboardButton("👤 Профиль")],
        [KeyboardButton("ℹ️ Помощь")]
     ]
)


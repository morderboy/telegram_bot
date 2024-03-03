from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

menu = [
    [InlineKeyboardButton(text="📝 Генерировать текст", callback_data="generate_text"),
    InlineKeyboardButton(text="🖼 Генерировать изображение", callback_data="generate_image")],
    [InlineKeyboardButton(text="💳 Купить токены", callback_data="buy_tokens"),
    InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
    [InlineKeyboardButton(text="💎 Партнёрская программа", callback_data="ref"),
    InlineKeyboardButton(text="🎁 Бесплатные токены", callback_data="free_tokens")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]

menu_admin = [
    [InlineKeyboardButton(text="Добавить токенов пользователю", callback_data="admin_tokens_add"),
    InlineKeyboardButton(text="Выйти из панели администратора", callback_data="exit_admin")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
menu_admin = InlineKeyboardMarkup(inline_keyboard=menu_admin)
buy_tokens_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💳 Купить токены", callback_data="buy_tokens")]])
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
confirmation_kb = ReplyKeyboardMarkup(keyboard=ReplyKeyboardBuilder().row(
    KeyboardButton(text="Да"),
    KeyboardButton(text="Нет")
).export(), resize_keyboard=True, one_time_keyboard=True)
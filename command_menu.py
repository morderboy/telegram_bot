from aiogram.types import BotCommand

bot_commands = [
    BotCommand(command="/start", description="Начать общение с ботом"),
    BotCommand(command="/menu", description="Выйти в меню бота"),
    BotCommand(command="/help", description="Помощь"),
    BotCommand(command="/ref", description="Ваша реферральная ссылка"),
    BotCommand(command="/balance", description="Количество доступных вам токенов"),
    BotCommand(command="/free_tokens", description="Получить в подарок бесплатные токены")
]
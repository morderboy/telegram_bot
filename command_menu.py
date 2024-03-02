from aiogram.types import BotCommand

bot_commands = [
    BotCommand(command="/start", description="Начать общение с ботом"),
    BotCommand(command="/menu", description="Выйти в меню бота"),
    BotCommand(command="/help", description="Помощь"),
    BotCommand(command="/ref", description="Ваша реферральная ссылка")
]
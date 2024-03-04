import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware

import config
from handlers import user_router, db
from admin import admin_router
from command_menu import bot_commands
from middlewares import banlist_middleware

async def main():
    bot = Bot(token=config.get_BotToken(), parse_mode=ParseMode.HTML)
    await bot.set_my_commands(commands=bot_commands)

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.outer_middleware(banlist_middleware)
    dp.callback_query.outer_middleware(banlist_middleware)
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.message.middleware(ChatActionMiddleware())
    
    await db.pre_process()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    asyncio.run(main())
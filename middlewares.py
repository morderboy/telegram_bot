from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import config
from loader import logger_admin

class AdminMiddleware(BaseMiddleware):
    def __init__(self)-> None:
        self.admins: list[int] = config.get_admin_ids()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
            ) -> Any:
                logger_admin.info(f"Попытка входа в панель администратора: username={event.from_user.username}; id={event.from_user.id}")
                if event.from_user.id in self.admins:
                    logger_admin.info(f"Администратор {event.from_user.username} c id {event.from_user.id} вошёл в панель.")
                    return await handler(event, data)
                
admin_middleware = AdminMiddleware()
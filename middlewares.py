from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import config
from loader import logger_admin, banlist

class AdminMiddleware(BaseMiddleware):
    def __init__(self)-> None:
        self.admins: list[int] = config.get_admin_ids()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
            ) -> Any:
                if event.from_user.id in self.admins:
                    return await handler(event, data)
                elif event.text == "/admin_start":
                    logger_admin.info(f"Попытка входа в панель администратора не администратором: username={event.from_user.username}; id={event.from_user.id}")
                else:
                    pass

class BanlistMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
         if event.from_user.id in banlist:
            await event.answer("Вы забанены")
         else:
            return await handler(event, data)
                
admin_middleware = AdminMiddleware()
banlist_middleware = BanlistMiddleware()
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import config

class AdminMiddleware(BaseMiddleware):
    def __init__(self)-> None:
        self.admins: list[int] = config.get_admin_ids()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
            ) -> Any:
                if event.user_id in self.admins:
                    return await handler(event, data)
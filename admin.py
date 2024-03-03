from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from middlewares import admin_middleware

admin_router = Router(name="admin")
admin_router.message.outer_middleware(admin_middleware)
admin_router.callback_query.outer_middleware(admin_middleware)

@admin_router.message(Command("admin_start"))
async def admin_start(msg: Message):
    await msg.answer(f"Привет админ: {msg.from_user.username}")
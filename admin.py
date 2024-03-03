from aiogram.filters import Command, CommandStart, CommandObject
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from middlewares import AdminMiddleware

router = Router(name="admin")
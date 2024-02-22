from aiogram import types, F, Router

from aiogram.types import Message
from aiogram.filters import Command

import message
import kb

router = Router()

@router.message(Command("start"))
async def start_handler(msg : Message):
    await msg.answer(message.get_start().format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg : Message):
    await msg.answer(message.get_menu(), reply_markup=kb.menu)
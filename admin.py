from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from middlewares import admin_middleware, logger_admin
from states import Admin

from kb import menu_admin, confirmation_kb
from loader import db
import config

admin_router = Router(name="admin")
admin_router.message.outer_middleware(admin_middleware)
admin_router.callback_query.outer_middleware(admin_middleware)

@admin_router.message(Command("admin_start"))
async def admin_start(msg: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Admin.start)
    logger_admin.info(f"Администратор {msg.from_user.username} зашёл в панель")
    await msg.answer(f"Привет админ: {msg.from_user.username}", reply_markup=menu_admin)

@admin_router.callback_query(F.data == "exit_admin")
async def admin_exit(clbk: CallbackQuery, state: FSMContext):
    await clbk.answer(f"До свидания {clbk.from_user.username}")
    await state.clear()

@admin_router.callback_query(F.data == "admin_tokens_add" and Admin.start)
async def add_tokens_start(clbk: CallbackQuery, state: FSMContext):
    await clbk.message.answer("Введите id пользователя которому хотите пополнить баланс")
    await state.set_state(Admin.enter_id)

@admin_router.message(Admin.enter_id)
async def enter_id(msg: Message, state: FSMContext):
    try:
        id = int(msg.text)
    except ValueError:
        return await msg.answer("Введите число")
    
    user = await db.get_username_by_id(id)
    if not user:
        await state.clear()
        return await msg.answer("Не верный id пользователя", reply_markup=menu_admin)
    
    await state.update_data(user_id=id)
    await state.set_state(Admin.enter_amount)
    await msg.answer("Введите количество (в рублях) на которое необходимо пополнить счёт пользователя")

@admin_router.message(Admin.enter_amount)
async def enter_amount(msg: Message, state: FSMContext):
    try:
        num = int(msg.text)
    except ValueError:
        return msg.answer("Введите число")
    
    await state.update_data(amount=num)
    await state.set_state(Admin.confirm)
    await msg.answer("Подтвердите свой выбор", reply_markup=confirmation_kb)

@admin_router.message(Admin.confirm)
async def add_tokens(msg: Message, state: FSMContext):
    if msg.text == "Да":
        data = await state.get_data()
        id = data["user_id"]
        tokens = config.get_tokens_per_rub() * data["amount"]
        await state.clear()
        await state.set_state(Admin.start)

        await db.add_tokens(user_id=id, tokens=tokens)
        logger_admin.info(f"Администратор {msg.from_user.username} добавил {tokens} токенов пользователю с id {id}")
        await msg.answer(f"Добавлено токенов: {tokens}", reply_markup=menu_admin)
    else:
        await state.clear()
        await state.set_state(Admin.start)
        await msg.answer("Выход в меню", reply_markup=menu_admin)
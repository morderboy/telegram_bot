from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext

import message
import kb
import utils
from states import Gen

router = Router()

@router.message(Command("start"))
async def start_handler(msg : Message):
    await msg.answer(message.get_message("start").format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg : Message):
    await msg.answer(message.get_message("menu"), reply_markup=kb.menu)

@router.callback_query(F.data == "generate_text")
async def state_gen_text(clbk: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_state)
    await clbk.message.edit_text(message.get_message("gen text"))
    await clbk.message.answer(message.get_message("gen text"), reply_markup=kb.exit_kb)

@router.message(Gen.text_state)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(message.get_message("gen wait"))
    res = await utils.generate_text(prompt=prompt)

    if not res:
        return await mesg.edit_text(text=message.get_message("gen error"), reply_markup=kb.iexit_kb)
    
    await mesg.edit_text(res[0] + message.get_message("text watermark"), disable_web_page_preview=True)

@router.callback_query(F.data == "generate_image")
async def state_gen_image(clbk: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.image_state)
    await clbk.message.edit_text(message.get_message("gen image"))
    await clbk.message.answer(message.get_message("gen image"), reply_markup=kb.exit_kb)

@router.message(Gen.image_state)
@flags.chat_action("typing")
async def generate_image(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(message.get_message("gen wait"))
    res = await utils.generate_image(prompt=prompt)

    if len(res) == 0:
        return await mesg.edit_text(text=message.get_message("gen error"), reply_markup=kb.iexit_kb)
    
    await mesg.delete()
    await mesg.answer_photo(photo=res[0], caption=message.get_message("img watermark"))
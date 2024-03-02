from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link, decode_payload

from yoomoney import Quickpay
import asyncio

import message
import kb
import utils
from states import Gen, Buy
from loader import db
import config
import uuid
import payment

router = Router()

@router.message(CommandStart())
async def start_handler(msg : Message, command: CommandObject):
    args = command.args
    await msg.answer(message.get_message("start").format(name=msg.from_user.full_name), reply_markup=kb.menu)
    if args:
        ref = int(decode_payload(args))
        success = await db.add_user(user_id=msg.from_user.id, username=msg.from_user.username, tokens=0, ref_id=ref)
        if success[-1] == "1":
            ref_username = await db.get_username_by_id(ref)
            await msg.answer(text="Удачно связан с пользователем @{}".format(ref_username['username']))
        else:
            await msg.answer(text="Не удалось привязать к пользователю")
    else:
        await db.add_user(user_id=msg.from_user.id, username=msg.from_user.username, tokens=0)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
@router.message(Command("menu"))
async def menu(msg : Message, state: FSMContext):
    await state.clear()
    await msg.answer(message.get_message("menu"), reply_markup=kb.menu)

@router.callback_query(F.data == "generate_text")
async def state_gen_text(clbk: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_state)
    await clbk.message.answer(message.get_message("gen text"), reply_markup=kb.exit_kb)

@router.message(Gen.text_state)
@flags.chat_action("typing")
async def generate_text(msg: Message):
    prompt = msg.text
    balance = await db.get_balance(msg.from_user.id)
    tokens_count = utils.num_tokens_from_messages(messages=[{"role": "user", "content": prompt}])

    if balance <= tokens_count:
        return await msg.answer(message.get_message("no money").format(tokens_count, balance), kb.iexit_kb)

    mesg = await msg.answer(message.get_message("gen wait"))
    res = await utils.generate_text(prompt=prompt)

    if not res:
        return await mesg.edit_text(text=message.get_message("gen error"), reply_markup=kb.iexit_kb)
    
    if balance < res[1]:
        return await msg.answer(message.get_message("no money").format(res[1], balance), kb.iexit_kb)
    
    await mesg.edit_text(res[0] + message.get_message("text watermark"), disable_web_page_preview=True)
    await db.pay_for_gen(msg.from_user.id, res[1])

@router.callback_query(F.data == "generate_image")
async def state_gen_image(clbk: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.image_state)
    await clbk.message.answer(message.get_message("gen image"), reply_markup=kb.exit_kb)

@router.message(Gen.image_state)
@flags.chat_action("typing")
async def generate_image(msg: Message):
    prompt = msg.text
    balance = await db.get_balance(msg.from_user.id)

    if balance < 10000:
        return await msg.answer(message.get_message("no money").format(10000, balance))

    mesg = await msg.answer(message.get_message("gen wait"))
    res = await utils.generate_image(prompt=prompt)

    if len(res) == 0:
        return await mesg.edit_text(text=message.get_message("gen error"), reply_markup=kb.iexit_kb)
    
    await mesg.delete()
    await mesg.answer_photo(photo=res[0], caption=message.get_message("img watermark"))
    await db.pay_for_gen(msg.from_user.id, 10000)

@router.message(Command("help"))
@flags.chat_action("typing")
async def help_command(msg: Message):
    await msg.answer(message.get_message("help"), reply_markup=kb.exit_kb)

@router.callback_query(F.data == "help")
@flags.chat_action("typing")
async def help_callback(clbk: CallbackQuery):
    await clbk.message.answer(message.get_message("help"), reply_markup=kb.exit_kb)

@router.callback_query(F.data == "buy_tokens")
@flags.chat_action("typing")
async def enter_amount(clbk: CallbackQuery, state: FSMContext):
    await clbk.message.answer(message.get_message("enter amount"), reply_markup=kb.exit_kb)
    await state.set_state(Buy.chooce_amount)

@router.message(Buy.chooce_amount)
@flags.chat_action("typing")
async def chooce_amount(msg: Message, state: FSMContext):
    try:
        num = int(msg.text)
        await state.update_data(amount=num)
        await state.set_state(Buy.confirmation)
        await msg.answer("Подтвердите выбор", reply_markup=kb.confirmation_kb)
    except ValueError:
        await msg.answer("Введити число", reply_markup=kb.exit_kb)
    

@router.message(Buy.confirmation)
async def confirmation_amount(msg: Message, state: FSMContext):
    if msg.text == 'Да':
        await msg.answer("Перейдите по ссылке для оплаты", reply_markup=kb.exit_kb)
        await buy_tokens(msg=msg, state=state)
        await state.clear()
    elif msg.text == 'Нет':
        await state.set_state(Buy.chooce_amount)
        await msg.answer("Введите сумму к оплате ещё раз", reply_markup=kb.exit_kb)

async def buy_tokens(msg: Message, state: FSMContext):
    amount_dict = await state.get_data()
    amount = amount_dict['amount']
    label = str(uuid.uuid4())
    quickpay = Quickpay(
            receiver=config.get_yoomoney_account_number(),
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=amount,
            label=label
            )
    await msg.answer(quickpay.redirected_url)

    order_id = await db.add_order(user_id=msg.from_user.id, label=label, amount=amount)

    try:
        await asyncio.wait_for(payment.payment_check(label=label), 12*60)
        await db.confirm_order(order_id=order_id)
        await db.add_tokens(user_id=msg.from_user.id, tokens=amount * 100)
    except asyncio.TimeoutError:
        await msg.answer("Где деньги либовски?")

@router.message(Command("ref"))
@flags.chat_action("typing")
async def ref_link_message(msg: Message):
    link = await create_start_link(bot=Bot.get_current(), payload=msg.from_user.id, encode=True)
    await msg.answer(text=link, reply_markup=kb.exit_kb)

@router.callback_query(F.data == "ref")
@flags.chat_action("typing")
async def ref_link_callback(clbk: CallbackQuery):
    link = await create_start_link(bot=Bot.get_current(), payload=clbk.from_user.id, encode=True)
    await clbk.message.answer(text=link, reply_markup=kb.exit_kb)

@router.message(Command("balance"))
@flags.chat_action("typing")
async def balance_message(msg: Message):
    balance = await db.get_balance(msg.from_user.id)
    await msg.answer(message.get_message("show balance").format(balance), reply_markup=kb.exit_kb)

@router.callback_query(F.data == "balance")
@flags.chat_action("typing")
async def balance_callback(clbk: CallbackQuery):
    balance = await db.get_balance(clbk.from_user.id)
    await clbk.message.answer(message.get_message("show balance").format(balance), reply_markup=kb.exit_kb)

@router.message(Command("free_tokens"))
@flags.chat_action("typing")
async def free_tokens_message(msg: Message):
    if config.get_free_tokens_state():
        user_id = msg.from_user.id
        is_used = await db.get_free_token_used(user_id)
        if is_used:
            await msg.answer(message.get_message("free tokens already used"), reply_markup=kb.exit_kb)
        else:
            tokens = config.get_free_tokens_amount()
            await db.add_tokens(user_id, tokens)
            await db.set_free_token_used(user_id, True)
            await msg.answer(message.get_message("free tokens give").format(tokens), reply_markup=kb.exit_kb)
    else:
        await msg.answer(message.get_message("no free tokens"), reply_markup=kb.exit_kb)

@router.callback_query(F.data == "free_tokens")
@flags.chat_action("typing")
async def free_tokens_callback(clbk: CallbackQuery):
    if config.get_free_tokens_state():
        user_id = clbk.from_user.id
        is_used = await db.get_free_token_used(user_id)
        if is_used:
            await clbk.message.answer(message.get_message("free tokens already used"), reply_markup=kb.exit_kb)
        else:
            tokens = config.get_free_tokens_amount()
            await db.add_tokens(user_id, tokens)
            await db.set_free_token_used(user_id, True)
            await clbk.message.answer(message.get_message("free tokens give").format(tokens), reply_markup=kb.exit_kb)
    else:
        await clbk.message.answer(message.get_message("no free tokens"), reply_markup=kb.exit_kb)
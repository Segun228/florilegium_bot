from app.handlers.router import router
import asyncio
import logging
import random
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext

from app.keyboards import inline as inline_keyboards

from app.states.states import Post

from aiogram.types import BufferedInputFile

from app.requests.user.login import login
from app.requests.helpers.get_cat_error import get_cat_error_async
#===========================================================================================================================
# Конфигурация основных маршрутов
#===========================================================================================================================

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    data = await login(telegram_id=message.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await message.answer("Ошибка авторизации, попробуйте позже 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await message.reply("Привет! 👋")
    await message.reply("Я бот платформы Florilegium. Я помогу вам выбрать и заказать лучшие экзотические растения")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)

@router.callback_query(F.data == "restart")
async def callback_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    data = await login(telegram_id=callback.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await callback.message.answer("Ошибка авторизации, попробуйте позже 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await callback.message.reply("Привет! 👋")
    await callback.message.reply("Я бот платформы Florilegium. Я помогу вам выбрать и заказать лучшие экзотические растения")
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(text="Этот бот помогает выбирать экзотические растения из нужных категорий\n\n Он может выполнять несколько интересных функций \n\nВы можете выбирать интересующие вас растения из категорий, имеющихся в наличии\n\nЕсли остались вопросы, пиши нашим менеджерам:\n\n@Elena_Noro\n\n@dianabol_metandienon_enjoyer", reply_markup=inline_keyboards.home)

@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback: CallbackQuery):
    await callback.answer()
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await callback.message.edit_text(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)


#===========================================================================================================================
# Взаимодействие с аккаунтом
#===========================================================================================================================
@router.callback_query(F.data == "account_menu")
async def account_menu_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Что вы хотите сделать с вашим аккаунтом? 👤", reply_markup=inline_keyboards.account_menu)


@router.callback_query(F.data == "delete_account_confirmation")
async def delete_account_confirmation_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Вы уверены что хотите удалить аккаунт? 😳 Восстановить записи будет невозможно... 🗑️", reply_markup=inline_keyboards.delete_account_confirmation_menu)


@router.callback_query(F.data == "delete_account")
async def delete_account_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_account(telegram_id=callback.from_user.id)
    await state.clear()
    await callback.message.edit_text("Аккаунт удален 😢", reply_markup=inline_keyboards.restart)



#===========================================================================================================================
# Заглушка
#===========================================================================================================================

@router.message()
async def all_other_messages(message: Message):
    await message.answer("Неизвестная команда 🧐")
    photo_data = await get_cat_error()
    if photo_data:
        photo_to_send = BufferedInputFile(photo_data, filename="cat_error.jpg")
        await message.bot.send_photo(chat_id=message.chat.id, photo=photo_to_send)

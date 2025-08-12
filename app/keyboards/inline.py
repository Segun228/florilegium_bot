from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Iterable

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Каталог", callback_data="catalogue")],
        [InlineKeyboardButton(text="👤 Аккаунт", callback_data="account_menu")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")]
    ]
)

account_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Админ", callback_data="admin_menu")],
        [InlineKeyboardButton(text="🗑️ Удалить аккаунт", callback_data="delete_account_confirmation")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)

delete_account_confirmation_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="delete_account")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="account_menu")],
    ]
)



home = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)

restart = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Главное меню", callback_data="restart")],
    ]
)


catalogue = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=" Каталог", callback_data="catalogue")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


async def get_catalogue(categories):
    keyboard = InlineKeyboardBuilder()
    if categories and categories is not None:
        for category in categories:
            keyboard.add(InlineKeyboardButton(text=category.get("name"), callback_data=f"category_{category.get('id')}"))
    keyboard.add(InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
    return keyboard.adjust(1).as_markup()


async def get_posts(posts, category):
    keyboard = InlineKeyboardBuilder()
    category_id = category.get("id", 0)
    if posts is None or posts == [] or posts == ():
        keyboard.add(InlineKeyboardButton(text="Каталог", callback_data="catalogue"))
        keyboard.add(InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
        return keyboard.adjust(1).as_markup()
    for post in posts:
        keyboard.add(InlineKeyboardButton(text=post.get("title", "Прекрасное растение"), callback_data=f"post_{category_id}_{post.get('id')}"))
    keyboard.add(InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
    return keyboard.adjust(1).as_markup()

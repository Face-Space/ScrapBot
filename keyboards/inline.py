from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# class MenuCallback(CallbackData, prefix="menu"):
#     category: str | None = None
#     price_filter: str | None = None

with open("E:/MyPetProjects/ScrapBot/scrap_data/categories_names.txt", encoding="utf-8") as file:
    src = [line.strip() for line in file.readlines()]

category_kb = InlineKeyboardBuilder()
for i in src:
    category_kb.add(InlineKeyboardButton(text=f"{i}", callback_data=f"{i}"))
category_kb.adjust(2, )


filter_price_kb = InlineKeyboardBuilder()
filter_price_kb.add(InlineKeyboardButton(text="Мин. цена", callback_data="min_price"))
filter_price_kb.add(InlineKeyboardButton(text="Макс. цена", callback_data="max_price"))
filter_price_kb.add(InlineKeyboardButton(text="Все товары категории", callback_data="all"))
filter_price_kb.add(InlineKeyboardButton(text="Назад", callback_data="back_to_menu"))
filter_price_kb.adjust(2, )


back_to_menu_kb = InlineKeyboardBuilder()
back_to_menu_kb.add(InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu"))
back_to_menu_kb.adjust(2, )

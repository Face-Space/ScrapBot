import asyncio

from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

import scraping
from FSM.states import NextStep

from keyboards.inline import category_kb, filter_price_kb, back_to_menu_kb
from utils.database import Database

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Здравствуйте, это ScrapBot. Помогу Вам спарсить цены с сайта. "
                         "Для начала скиньте сюда своё сообщение, содержащее ссылку на сайт:")


@user_private_router.message(StateFilter(None), F.text.contains("https://www.forward-sport.ru/"))
async def message_link(message: types.Message, state: FSMContext):
    await message.answer("Парсинг сайта начался, пожалуйста подождите...")
    # Выполняем scraping.main() в отдельном потоке
    # await asyncio.get_running_loop().run_in_executor(None, scraping.main)
    await message.answer("Цены спарсены. Выберите нужную Вам категорию:", reply_markup=category_kb.as_markup())
    await state.set_state(NextStep.choose_category)


@user_private_router.callback_query(F.data == "back_to_menu")
async def back_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Вы вернулись обратно в меню. Выберите категорию:", reply_markup=category_kb.as_markup())
    await state.set_state(NextStep.choose_category)


@user_private_router.callback_query(NextStep.choose_category, F.data)
async def new_collection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(category=callback.data)
    data = await state.get_data()
    await callback.message.answer(f'Хорошо, теперь задайте фильтр для категории "{data["category"]}":',
                                  reply_markup=filter_price_kb.as_markup())
    await state.set_state(NextStep.set_filter)


@user_private_router.callback_query(NextStep.set_filter, F.data)
async def set_my_filter(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(my_filter=callback.data)
    data = await state.get_data()
    db = Database(f"scrap_data/{data["category"]}/products_page.db")

    if data["my_filter"] == "min_price":
        product_info = list(db.get_min_price())
        # image = (InputMediaPhoto(media="https://www.forward-sport.ru/" + f"{product_info[1]}", caption=product_info[2]))
        for item in product_info:
            url = "https://www.forward-sport.ru" + f"{item[1]}"
            await callback.message.answer_photo(url, caption=f"{item[2]}\n{round(item[3])} руб.")

        await callback.message.answer(f'Вот минимальная цена товара из категории "{data["category"]}":',
                                      reply_markup=back_to_menu_kb.as_markup())


    elif data["my_filter"] == "max_price":
        product_info = list(db.get_max_price())
        for item in product_info:
            url = "https://www.forward-sport.ru" + f"{item[1]}"
            await callback.message.answer_photo(url, caption=f"{item[2]}\n{round(item[3])} руб.")

        await callback.message.answer(f'Вот 3 максимальные цены товара из категории "{data["category"]}":',
                                      reply_markup=back_to_menu_kb.as_markup())

    elif data["my_filter"] == "all":
        product_info = list(db.get_all_products())
        for item in product_info:
            url = "https://www.forward-sport.ru" + f"{item[1]}"
            await callback.message.answer_photo(url, caption=f"{item[2]}\n{round(item[3])} руб.")

        await callback.message.answer(f'Вот цены на все товары из категории "{data["category"]}":',
                                      reply_markup=back_to_menu_kb.as_markup())

    await state.clear()


@user_private_router.message()
async def misunderstand(message: types.Message):
    await message.answer("Пришлите сообщение, содержащее ссылку на сайт, с которого нужно спарсить "
                         "цены либо проверьте правильность ссылки!")


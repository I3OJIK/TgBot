from aiogram import F, Router, types

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboards as kb

from app.api_client import get_access_token, get_cart, change_product_quantity


class Reg(StatesGroup):
    name = State()
    number = State()


router = Router()

# message.reply - отправляет как ответ на сообщение
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Здарова еп.\n Твой ID: {message.from_user.id}\n Твое имя: {message.from_user.full_name}',
                        reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Команда /help')

@router.message(Command('token'))
async def get_help(message: Message):
    token = await get_access_token()
    await message.answer(f'Token:\n {token}')


@router.message(Command('cart'))
async def send_cart(message: types.Message):
    token = await get_access_token()
    if not token:
        await message.answer("❌ Не удалось получить токен")
        return

    cart_data = await get_cart(token)
    if "data" not in cart_data or not cart_data["data"]:
        await message.answer("🛒 Корзина пуста")
        return

    await message.answer(
        "🛒 Ваша корзина:",
        reply_markup=kb.build_cart_keyboard(cart_data)
    )

async def update_cart_message(callback: CallbackQuery):
    token = await get_access_token()
    cart_data = await get_cart(token)

    if "data" not in cart_data or not cart_data["data"]:
        new_text = "🛒 Корзина пуста"
        new_markup = None
    else:
        new_text = "🛒 Ваша корзина:"
        new_markup = kb.build_cart_keyboard(cart_data)
        
    await callback.message.edit_text(new_text, reply_markup=new_markup)

@router.callback_query(F.data.startswith("decrease:"))
async def on_decrease_callback(callback: CallbackQuery):
    product_id = callback.data.split(":")[1]
    delta = -1
    await change_product_quantity(product_id, delta)
    await update_cart_message(callback)
    await callback.answer("Уменьшили количество товара")


@router.callback_query(F.data.startswith("increase:"))
async def on_increase_callback(callback: CallbackQuery):
    product_id = callback.data.split(":")[1]
    delta = 1
    await change_product_quantity(product_id, delta)
    await update_cart_message(callback)
    await callback.answer("Увеличили количество товара")


# Ловим с помощью F.text определенный текст от пользователя
@router.message(F.text == 'Как дела?') 
async def how_are_you(message: Message):
    await message.answer('Харашо')

# photo[-1] - вытаскиваем айди лучшего качества
@router.message(F.photo) 
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')

@router.message(F.text == 'Покажи мартышку')
async def get_help(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMeaJtcsae0aUCJ5F2OnQ9aG1xecGEAAnv1MRvm2NlIWIVbjWcKxGYBAAMCAAN5AAM2BA',
                               caption='Мартышка')
    
# поэтапное выполнение (сначало ввод имени потом телефон)
@router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите имя')
# получение JWT токена, вывод корзины, изменение колва товара в корзине, функции для обучения
@router.message(Reg.name)
async def reg_two(message: Message,state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона')

@router.message(Reg.number)
async def reg_three(message: Message,state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Шпасеба\n Имя: {data["name"]}\n телефон: {data["number"]}')
    await state.clear()
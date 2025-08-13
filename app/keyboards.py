from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton,InlineKeyboardMarkup)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    
        [KeyboardButton(text='Покажи мартышку')],
        [KeyboardButton(text='Корзина'),KeyboardButton(text='Контакты')]
    
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт меню...')

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='YouTube', url='https://youtube.com')]
])


# билдер для динамического создания кнопок
def build_cart_keyboard(cart_data):
    keyboard = InlineKeyboardBuilder()
    for item in cart_data["data"]:
        product = item.get("product", {})
        color = item.get("color", {})
        product_id = item.get("id")
        keyboard.row(
            InlineKeyboardButton(
                text=f"{product.get('name', 'Без названия')} {color.get('name', '')} ({item.get('quantity')} шт.)",
                callback_data=f"edit_{item.get('id')}"
            )
        )
        keyboard.row(
            InlineKeyboardButton(text=f"-", callback_data=f"decrease:{product_id}"),
            InlineKeyboardButton(text=f"+", callback_data=f"increase:{product_id}")
        )

    return keyboard.as_markup()

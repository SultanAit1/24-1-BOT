from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import text

start_markup = InlineKeyboardMarkup(row_width=4)
one = InlineKeyboardButton(text='информация о компании', callback_data="one")
three = InlineKeyboardButton(text='Наши контакты', callback_data='three')
two = InlineKeyboardButton(text='партнерство', callback_data='two')
last = InlineKeyboardButton(text='Админ', callback_data='last', url="https://t.me/xmTenZenE")
start_markup.add(one)
start_markup.add(two)
start_markup.add(three)
start_markup.add(last)

main_markup = InlineKeyboardMarkup(row_width=1)
exit_1 = InlineKeyboardButton(text="Вернуться в Меню", callback_data='exit_1')
main_markup.add(exit_1)


url_markup = InlineKeyboardMarkup(row_width=4)
russia = InlineKeyboardButton(text='Товары России', callback_data='russia', url='https://www.apple.com/ru/iphone/')
kazax = InlineKeyboardButton(text='Товары Казахстана', callback_data='kazax', url="https://www.samsung.com/ru/")
uzb = InlineKeyboardButton(text='Товары Узбекистана', callback_data='uzb',url="https://mi-shop.kg/")
url_markup.add(russia)
url_markup.add(kazax)
url_markup.add(uzb)
url_markup.add(exit_1)

spam_markup= InlineKeyboardMarkup(row_width=2)
confirm = InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm,{text}')
cancel = InlineKeyboardButton(text='Отмена', callback_data='cancel')
spam_markup.add(cancel, confirm)



from aiogram.types import InlineKeyboardButton, CallbackQuery
from config import bot, dp
from keyboards.client_kb import start_markup, main_markup, url_markup, profil_markup
import sqlite3

from aiogram import  Dispatcher, types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_start = State()



conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER PRIMARY KEY)
                """)
conn.commit()


# noinspection SqlResolve
@dp.message_handler(content_types=['voice'])
async def handle_voice(message: types.Message):
    if message.from_user.id != 661114436:
        return
        voice_id = message.voice.file_id
        try:
            # Отправляем фото всем подписчикам
            cursor.execute("SELECT user_id FROM users")
            rows = cursor.fetchall()
            for row in rows:
                user_id = row[0]
                await bot.send_voice(chat_id=user_id, voice=voice_id)
                await message.answer(f" voice успешно отправлено всем подписчикам ({len(rows)} человек).")
        except Exception as e:
            print(f"Ошибка при отправке видео: {e}")


# noinspection SqlResolve
@dp.message_handler(content_types=['video_note'])
async def handle_note(message: types.Message):
    if message.from_user.id != 661114436:
        return
        video_note_id = message.video_note.file_id
        try:
            # Отправляем фото всем подписчикам
            cursor.execute("SELECT user_id FROM users")
            rows = cursor.fetchall()
            for row in rows:
                user_id = row[0]
                await bot.send_video_note(chat_id=user_id, video_note=video_note_id)
                await message.answer(f"Видео успешно отправлено всем подписчикам ({len(rows)} человек).")
        except Exception as e:
            print(f"Ошибка при отправке видео: {e}")


# noinspection SqlResolve
@dp.message_handler(content_types=['video'])
async def handle_video(message: types.Message):
    # Получаем идентификатор фото
    video_id = message.video.file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_video(chat_id=user_id, video=video_id,caption=message.caption[6:] )
        await message.answer(f"Видео успешно отправлено всем подписчикам ({len(rows)} человек).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")

# noinspection SqlResolve
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    # Получаем идентификатор фото
    photo_id = message.photo[-1].file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_photo(chat_id=user_id, photo=photo_id,caption=message.caption[6:] )
        await message.answer(f"Фото успешно отправлено всем подписчикам ({len(rows)} человек).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")

# noinspection SqlResolve,PyUnboundLocalVariable
@dp.message_handler(commands=['/spam'])
async def spam_commands(message: types.Message):

    if message.from_user.id != 661114436:

        await message.answer("Вы не являетесь администратором.")
        return
    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]

        try:
            if message.photo:
                photo_id = message.photo[-1].file_id
                photo_obj = await bot.get_file(photo_id)
                photo = photo_obj.download()
                await bot.send_photo(chat_id=user_id, photo=open(photo, 'rb'), caption=message.caption[6:] )
            elif message.video:
                video_id = message.video.file_id
                await bot.send_video(chat_id=user_id, video=video_id, caption=message.caption[6:])
            else:
                await bot.send_message(chat_id=user_id, text=message.text[6:])
        except Exception as e:
            print(f"Ошибка при отправке сообщения для пользователя {rows}: {e}")
        await message.answer(f"Сообщение успешно отправлено всем подписчикам ({len(user_id)} человек).")

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    cursor.execute("INSERT OR REPLACE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    if message.from_user.id != 661114436:
        await bot.send_message(chat_id=message.from_user.id, text='https://youtu.be/UCF1oebyXMQ\n')
        await bot.send_message(chat_id=message.from_user.id,
                                                             text=
                                                                  "\n*😎Это главное меню "
                                                                  'автоматизированной системы '
                                                                  'с элементами искусственного интеллекта и отсюда '
                                                                  'мы с тобой можем узнать ВСЕ о компании c МИРОВЫМ именем - ERSAG!\n'
                                                
                                                                  '\n➡️Сразу оставлю контакты моего владельца, к '
                                                                  'которому ты всегда можешь обратиться если у тебя '
                                                                  'будут вопросы:\n  '
                                                                  '\n✳️✳️✳️* '
                                                        
                                                                  '\n@Pomoshnikersag\n    '
                        
                                                                  '\n*Ты всегда можешь обратиться к нему и получить'
                                                                  ' ответы на все вопросы: \n '
                                                                  '\n💡А теперь просто выбирай по кнопкам что тебе '
                                                                  'интересно и я все расскажу*) \n '
             ''                                                      '⬇️⬇️⬇️'
                               ,
        reply_markup=start_markup)

    else:
        await bot.send_message(chat_id=message.from_user.id, text='https://youtu.be/UCF1oebyXMQ\n')
        await bot.send_message(chat_id=message.from_user.id, text=
                                                                  '\n*😎Это главное меню '
                                                                  'автоматизированной системы '
                                                                  'с элементами искусственного интеллекта и отсюда '
                                                                  'мы с тобой можем узнать ВСЕ о компании c МИРОВЫМ именем - ERSAG!\n'
                                                
                                                                  '\n➡️Сразу оставлю контакты моего владельца, к '
                                                                  'которому ты всегда можешь обратиться если у тебя '
                                                                  'будут вопросы:\n  '
                                                                  '\n✳️✳️✳️* '
                                                        
                                                                  '\n@Pomoshnikersag\n    '
                        
                                                                  '\n*Ты всегда можешь обратиться к нему и получить'
                                                                  'ответы на все вопросы: \n '
                                                                  '\n💡А теперь просто выбирай по кнопкам что тебе '
                                                                  'интересно и я все расскажу*) \n '
                                                                  '⬇️⬇️⬇️',reply_markup=profil_markup)
    await UserStates.waiting_for_start.set()
    await state.update_data(user_id=message.from_user.id, username=message.from_user.username)
    # отправляем уведомление администратору
    await bot.send_message(661114436,
                           f"Пользователь {message.from_user.id} (@{message.from_user.username}) начал использовать бота")


@dp.callback_query_handler(text="one")
async def one(callback: CallbackQuery):
    one = InlineKeyboardButton("one", callback_data="one")
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id ,
   text='Сегодня тысячи людей во всем мире заботятся'
        'о своем здоровье и окружающей среде,\n поэтому сделали свой выбор за ЭКО товарами!\n '
        '\n😇Компания ERSAG основана в 2002 году в Турции г. Денизли '
        'и производит натуральную продукцию на основе мыльных орехов и других растительных экстрактов.\n '
        '\nПроизводственные базы продукции находятся в Турции и насчитывают 6 фабрик. '
        'Каждая из которых производит определенную продукцию:\n '
        'чистящие-моющие средства, средства личной гигиены (крема, шампуни и т.д.), '
        'декоративная косметика, БАДы, кофе, чай, масла холодного отжима и косметические масла, парфюмерия.\n '
        '\n😎20 лет Ersag успешно реализует продукцию в 14 странах мира в том числе и Европейский рынок. \n'
        'Вся продукция Ersag органическая, не содержит химических и синтетических соединений и добавок, '
        'растительных жиров, отдушек, парабенов, лаурильсульфатов, фосфатов, фтора. \n'
        '\nНа свою продукцию компания получила 14 международных сертификатов! HALAL, ECO CERT, ISO, GMP, OHRAS, BIO, ECO, и другие.\n'
        '\nВся упаковка для продукции экологически чистая, и изготовлена '
        'из специального пластика который полностью разлагается, '
        'не причиняя ущерба окружающей среде. ' ,reply_markup=main_markup)




@dp.callback_query_handler(text="two")
async def two(callback: CallbackQuery):
    two = InlineKeyboardButton('two', callback_data='two')
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,
                                text="😇Маркетинг план ERSAG - и много 'плюшек' сразу для тебя:\n"
                                     "\n✅1. Бесплатная регистрация на сайте компании и с"
                                     "первого заказа уже скидка в 20%. "
                                     "При каждом заказе получаете подарков на сумму заказа.\n"
                                     "\n✅2. Карьерная скидка плюсуются к партнерской цене, "
                                     "чем выше карьера тем больше личная скидка на заказ. \n "
                                     "\n✅3.Фиксированная карьера, никогда не падаешь ниже со статуса."
                                     "Даже если делаешь заказ через год. \n"
                                     "\n✅4.Ежемесячная активность: либо личный объём"
                                     "согласно карьеры либо подключение нового человека "
                                     "в первую линию с заказом от 2 баллов.\n "
                                     "\n✅5.Возможность закрывать карьеру за два месяца.\n"
                                     "\n✅6. Переход баллов из предыдущего месяца в действующий.  \n"
                                     "\n✅7.Возможность закрытия карьеры в любой день "
                                     "месяца и несколько карьер от 10% до 33% за месяц.\n "
                                     "\n✅8. Выплаты со всей структуры и глубины  \n"
                                     "\n✅9. Лидерский бонус \n "
                                     "\n✅10. Нет обрезания лидеров по маркетингу \n "
                                     "\n✅11. Ежемесячные официальные выплаты премии на карточку \n "
                                     "\n✅12. Международный бизнес  \n"
                                     "\n✅13. При заказе в день рождения компания дарит дополнительный подарок \n " , reply_markup=main_markup   )


@dp.callback_query_handler(text="three")
async def three(callback: CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id ,text="😍В компании огромный ассортимент продукции,\n"
                                                                                                              "и для твоего удобства, я прикрепил несколько "
                                                                                                              "каталогов, которыe ты можешь посмотреть)\n  "
                                                                                                              "\n😎Если тебе нужен каталог именно для твоей страны "
                                                                                                              "проживания, \n просто напиши моему владельцу сюда - и "
                                                                                                              "он поможет тебе в этом вопросе!  "
                                                                                                              "\n✳️✳️✳️  "
                                                                                                              "\n@Pomoshnikersag \n",

                          reply_markup=url_markup, )


@dp.callback_query_handler(text="last")
async def last(message: types.Message, ):
    last = InlineKeyboardButton('last', callback_data='last')
    await bot.send_message(chat_id=message.from_user.id, text="Хочу такого бота себе♻️")

@dp.callback_query_handler(text='four')
async def four(callback: CallbackQuery):
    four = InlineKeyboardButton('four', callback_data='four')
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id , text="Система продвижения в нашем сообществе уникальна и она включает в себя: \n "
                                                                                                 "\n✅ пошаговое обучение и сопровождение каждого "
                                                                                                 "партнера, доведение до результата!\n  "
                                                                                                 "\n✅ использование эффективных систем, в том числе "
                                                                                                 "автоматизированных, например как я)\nТакой "
                                                                                                 "ассистент есть у каждого нашего партнера и будет доступен и тебе! \n "
                                                                                                 "\n✅ готовые алгоритмы для работы, скрипты диалогов, "
                                                                                                 "эффективные инструменты \n "
                                                                                                 "\n✅ использование сочетания работы и 'на земле' и в" 
                                                                                                 "онлайне - подойдет для любого человека! \n "
                                                                                                 "\n🤑 Идем все вместе, одной сильной командой!\n"
                                                                                                 "Для каждого человека - это огромные перспективы и возможности!\n  "
                                                                                                 "\n😎  Для получения большей информации жми кнопку главное меню! ",
                          reply_markup=main_markup, )

@dp.callback_query_handler(text='five')
async def five(callback: CallbackQuery):
    five = InlineKeyboardButton('five', callback_data='five')
    await bot.edit_message_text(chat_id=callback.message.chat.id ,message_id=callback.message.message_id, text="😃Чтобы стать партнером компании, \nпросто напиши моему владельцу, вот его контакты:"
                                                                                                               "\n✳️✳️✳️     \n"
                                                                                    
                                                                                                 "\n@Pomoshnikersag \n"
                                                                                                 "\nСвяжись с ним и он поможет тебе правильно\n"
                                                                                                 "зарегистрироваться и грамотно запуститься в "
                                                                                                 "компании! 🤝\n"
                                                                                                 "\nЕсли я могу тебе еще чем-то помочь, то переходи в "
                                                                                                 "главное меню - я полностью к твоим услугам!" ,reply_markup=main_markup   )


@dp.callback_query_handler(text="exit_1")
async def exit_1(callback: CallbackQuery):
    exit_1 = InlineKeyboardButton('exit_1', callback_data="exit_1")
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id, text=

    '*😎Это главное меню '
    
    ' автоматизированной системы'
    ' с элементами искусственного интеллекта и отсюда'
    ' мы с тобой можем узнать ВСЕ о компании c МИРОВЫМ именем - ERSAG!\n'

    '\n➡️Сразу оставлю контакты моего владельца, к '
    'которому ты всегда можешь обратиться если у тебя '
    'будут вопросы:\n  '
    '\n✳️✳️✳️* '

    '\n@Pomoshnikersag\n    '

    '\n*Ты всегда можешь обратиться к нему и получить'
    ' ответы на все вопросы: \n '
    '\n💡А теперь просто выбирай по кнопкам что тебе '
    'интересно и я все расскажу*) \n '
    '⬇️⬇️⬇️',
                           reply_markup=start_markup)


@dp.callback_query_handler(text="comand")
async def comand(callback: CallbackQuery):
    comand = InlineKeyboardButton('comand', callback_data='comand')
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,
                                text="основное меню - /start;\n"
                                   '\nКружочки в тг - автоматически;\n'
                                   '\nфото с текстом - /spam; \n'
                                   '\nвидео с текстом - /spam;\n'
                                   '\nголосовое сообщение - автоматически.\n',
                                reply_markup=main_markup

    )

@dp.message_handler(commands=["follow"])
async def get_subscribers_count(message: types.Message):
    if message.from_user.id != (await bot.get_chat_member(message.chat.id, message.from_user.id)).user.id:
        return
    count = await bot.get_chat_members_count(message.chat.id)
    await message.answer(f"количество подписчиков бота: {count}")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(handle_note, commands=['note'])
    dp.register_message_handler(spam_commands, commands=['spam'])
    dp.register_message_handler(handle_voice, commands=['voice'])
    dp.register_message_handler(get_subscribers_count, commands=['follow'])
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(handle_video, commands=['spam'])
    dp.register_message_handler(handle_photo, commands=['spam'])
    dp.callback_query_handler(four, text='four')
    dp.callback_query_handler(five, text='five')
    dp.callback_query_handler(one, text='one')
    dp.callback_query_handler(two, text='two')
    dp.callback_query_handler(three, text='three')
    dp.callback_query_handler(last, text='last')
    dp.callback_query_handler(exit_1, text='exit_1')
    dp.callback_query_handler(comand, text='comand')







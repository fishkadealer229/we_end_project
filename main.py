import logging
import requests
import os
from time import sleep
from config import token
from aiogram import Bot, Dispatcher, executor, types
bot = Bot(token=token)
dp = Dispatcher(bot)
db_values = []
register_flag = False
admin_flag = False
search_flag = False
update_flag = False
new_value = True
mesage = False
flag = False
flag1 = True
flag2 = False
photo_flag = False
stop = False
authorize_flag = False
password = ''
update_value = ''
count_values = 1
last_username = ''
mes_id = ''
value1 = 0
json = {}
admin_chat_id = 1103098407
blank_values = ["Имя Фамилия", "Пол", "Юзернейм", 'Должность', 'Пароль']
asks = ['своё имя и фамилию', 'свой пол', 'свой юзернейм', "свою должность в компании", 'свой пароль']
ind = 0
logging.basicConfig(level=logging.INFO)


async def set_default_commands():
    global dp
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("menu", "Меню")])


@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    global db_values, register_flag, admin_flag, search_flag, update_flag, new_value, flag, flag1, flag2, photo_flag
    global stop, password, update_value, count_values, last_username, ind, authorize_flag, value1
    await set_default_commands()
    db_values = []
    register_flag = False
    admin_flag = False
    search_flag = False
    update_flag = False
    new_value = True
    flag = False
    flag1 = True
    flag2 = False
    photo_flag = False
    stop = False
    authorize_flag = False
    password = ''
    update_value = ''
    count_values = 1
    last_username = ''
    ind = 0
    response = requests.get(f'http://127.0.0.1:5000/staff_api/user/id/{message.from_user.id}')
    if response:
        response = response.json()
        status = response['status']  # bool
        is_admin = response['is_admin']  # bool
        if is_admin:
            admin_flag = True
        if status:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.insert(types.InlineKeyboardButton(text='Да', callback_data='search'))
            keyboard.insert(types.InlineKeyboardButton(text='Нет', callback_data='ok'))
            await message.answer('Хотите кого-то найти?', reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.insert(types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='common'))
            keyboard.insert(types.InlineKeyboardButton(text='Войти', callback_data='authorize'))
            await message.answer('Здравствуйте! Я бот для связи между сотрудниками одной компании, созданный компанией'
                                 ' "Нигэз Студио".', reply_markup=types.ReplyKeyboardRemove())
            await message.answer('Мы не нашли вас в списках компании, поэтому предлагаем зарегистрироваться или войти',
                                 reply_markup=keyboard)
    else:
        await message.answer('Извините, произошла ошибка')
        await message.answer(f'"Http статус:", {response.status_code}, "(", {response.reason}, ")")')


@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    if stop:
        await message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.insert(types.InlineKeyboardButton(text='Зарегестрироваться', callback_data='common'))
        keyboard.insert(types.InlineKeyboardButton(text='Войти', callback_data='authorize'))
        keyboard.add(types.InlineKeyboardButton(text='Поиск', callback_data='search'))
        keyboard.add(types.InlineKeyboardButton(text='Изменить свою анкету', callback_data='update_blank'))
        await message.answer('Вот, что может этот ботяра.', reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help1(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Как мне зарегистрироваться?', callback_data='register_help'))
    keyboard.add(types.InlineKeyboardButton(text='Как стать админом?', callback_data="admin_moment"))
    keyboard.add(types.InlineKeyboardButton(text='Как попасть к вам в компанию?', callback_data='new_workers'))
    keyboard.add(types.InlineKeyboardButton(text='Другое', callback_data='other'))
    await message.answer("Здравствуйте. Какой вопрос у вас возник?", reply_markup=keyboard)


@dp.callback_query_handler(text='register_help')
async def register_help(call: types.CallbackQuery):
    await call.message.answer('Просто напишите /menu , затем выбирете "Зарегестрироваться" и выполняйте инструкции')


@dp.callback_query_handler(text='admin_moment')
async def admin_moment(call: types.CallbackQuery):
    await call.message.answer('По таким вопросам нужно писать этому прекрасному человеку: @BenzopilaVitalij')


@dp.callback_query_handler(text='new_workers')
async def new_workers(call: types.CallbackQuery):
    await call.message.answer('Извините, пока нам новые работники не нужны)')


@dp.callback_query_handler(text='other')
async def other(call: types.CallbackQuery):
    global mesage
    mesage = True
    await call.message.answer('Напишите сообщение которое будет передано админу')


@dp.callback_query_handler(text='common')
async def register_asks(call: types.CallbackQuery):
    global asks, ind, stop
    if stop:
        await call.message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        ln = 0
        if call.from_user.last_name:
            ln = call.from_user.first_name + " " + call.from_user.last_name
        else:
            ln = call.from_user.first_name
        telegram_values = [ln, 'Мужчина',
                           call.from_user.username, '', '', '']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if ind <= 2:
            if len(telegram_values[ind]) != 0:
                keyboard.add(types.KeyboardButton(text=f'{telegram_values[ind]}'))
            else:
                await call.message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
                stop = True
        if ind == 1:
            keyboard.add(types.KeyboardButton(text='Женщина'))
        if ind < len(asks):
            await call.message.answer(f'Укажите {asks[ind]}', reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='update_blank'))
            keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='end_register'))
            await call.message.answer('Хотите изменить анкету?', reply_markup=keyboard)


@dp.callback_query_handler(text='authorize')
async def authorize(call: types.CallbackQuery):
    global authorize_flag, value1
    if stop:
        await call.message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        authorize_flag = True
        if value1 == 0:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(types.KeyboardButton(text=call.from_user.username))
            await call.message.answer('Итак авторизация...')
            await call.message.answer('Введите свой юзернейм', reply_markup=keyboard)
        else:
            await call.message.answer('Введите свой пароль', reply_markup=types.ReplyKeyboardRemove())
        await call.answer()


@dp.callback_query_handler(text='update_blank')
async def update_blank(call: types.CallbackQuery):
    global blank_values, update_flag, register_flag, search_flag, flag1
    if stop:
        await call.message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        if len(db_values) == 0:
            await begin(call.message)
        else:
            register_flag = False
            search_flag = False
            update_flag = True
            flag1 = True
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for i in blank_values:
                keyboard.add(types.KeyboardButton(text=f'{i}'))
            await call.message.answer('Что вас не устраивает?', reply_markup=keyboard)
            await call.answer()


@dp.callback_query_handler(text='end_register')
async def end_register(call: types.CallbackQuery):
    global register_flag, admin_flag, update_flag, search_flag
    if stop:
        await call.message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        if len(db_values) == 0:
            await begin(call.message)
        else:
            data = f'{db_values[0]}/{db_values[1]}/{db_values[2]}/{db_values[3]}/{call.from_user.id}/{admin_flag}/' \
                   f'{db_values[4]}'
            response = requests.get(f'http://127.0.0.1:5000/staff_api/end_register/{data}')
            if response:
                response = response.json()
                if response['success']:
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.insert(types.InlineKeyboardButton(text='Да', callback_data='search'))
                    keyboard.insert(types.InlineKeyboardButton(text='Нет', callback_data='ok'))
                    await call.message.answer('Хотите кого-то найти?', reply_markup=keyboard)
                    await call.answer()
                    register_flag = True
                    search_flag = False
                    update_flag = False
                else:
                    await call.message.answer(f'К сожалению мы не смогли сохранить ваши даннные.')
                    await call.message.answer(response['error'])
            else:
                await call.message.answer(f'К сожалению мы не смогли сохранить ваши даннные. Произошла ошибка')
                await call.message.answer(f'"Http статус:", {response.status_code}, "(", {response.reason}, ")")')


@dp.callback_query_handler(text='search')
async def search(call: types.CallbackQuery):
    global search_flag, register_flag, update_flag
    if stop:
        await call.message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        search_flag = True
        register_flag = False
        update_flag = False
        await call.message.answer("Введите данные для поиска (Имя Фамилия или должность)")


@dp.callback_query_handler(text='ok')
async def ok(call: types.CallbackQuery):
    if stop:
        await call.message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Искать кого-то...', callback_data='search'))
        await call.message.answer('Ну ок...', reply_markup=keyboard)
        await call.answer('OK')


@dp.message_handler(content_types=['text'])
async def db_insert(message: types.Message):
    global db_values, register_flag, search_flag, update_flag, flag1, flag2, new_value, update_value, stop, value1, json
    global authorize_flag, mesage
    if mesage:
        await bot.send_message(admin_chat_id, text=f'Сообщение от @{message.from_user.username}:\n"{message.text}"')
        await message.answer('Спасибо за ваше сообщение.')
        mesage = False
    else:
        if message.message_id != mes_id:
            if stop:
                await message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
            else:
                if register_flag:
                    await message.reply('Эу нормально общайся. ОК?')
                elif search_flag:
                    response = requests.get(f'http://127.0.0.1:5000/staff_api/search/<str:{message.text}>')
                    if response:
                        response = response.json()
                        success = response['success']
                        if success:
                            name, surname = response['name_surname'].split()  # str
                            gender = response['gender']  # str
                            username = response['username']  # str
                            username = '@' + username
                            profession = response['profession']  # str
                            user_id = response['user_id']  # str
                            photo_path = f'\\photos\\{user_id}.jpg'
                            text = f'Имя: {name}\nФамилия: {surname}\nПол: {gender}\nДолжность: {profession}\n{username}'
                            await bot.send_photo(message.chat.id, types.InputFile(photo_path), caption=text)
                            keyboard = types.InlineKeyboardMarkup()
                            keyboard.insert(types.InlineKeyboardButton(text='Да', callback_data='search'))
                            keyboard.insert(types.InlineKeyboardButton(text='Нет', callback_data='ok'))
                            await message.answer('Хотите кого-то найти?', reply_markup=keyboard)
                        else:
                            await message.answer('К сожалению, по эти данным ничего не найдено:(')
                            # await message.answer(f'{response["value"]}={response["search_text"].strip()[5:-1]}')
                            # await message.answer
                    else:
                        await message.answer('Извините, произошла ошибка')
                        await message.answer(f'Http статус: {response.status_code} ({response.reason})')
                    search_flag = False
                elif update_flag:
                    new_value = True
                    if new_value and message.text in blank_values:
                        update_value = message.text
                        new_value = False
                        flag1 = True
                    else:
                        if flag1:
                            db_values[blank_values.index(update_value)] = message.text
                            flag1 = False
                        else:
                            flag2 = True
                    if flag1:
                        await message.answer('Хорошо', reply_markup=types.ReplyKeyboardRemove())
                        if message.text != "Фотография":
                            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                            if update_value == 'Пол':
                                keyboard.add(types.KeyboardButton(text='Женщина'))
                                keyboard.add(types.KeyboardButton(text='Мужчина'))
                            elif update_value == 'Пароль':
                                pass
                            else:
                                keyboard.add(types.KeyboardButton(text=f'{db_values[blank_values.index(update_value)]}'))
                            await message.answer('Введите новое значение.', reply_markup=keyboard)
                        else:
                            await message.answer('Отлично', reply_markup=types.ReplyKeyboardRemove())
                            keyboard = types.InlineKeyboardMarkup()
                            keyboard.add(types.InlineKeyboardButton(text='Оставить прежнию', callback_data='next_data'))
                            await message.answer('Отправьте новую фотографию', reply_markup=keyboard)
                    else:
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='update_blank'))
                        keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='end_register'))
                        await message.answer('Ваши данные успешно сохранены', reply_markup=types.ReplyKeyboardRemove())
                        await message.answer('Хотите ещё что-нибудь изменить?', reply_markup=keyboard)
                elif authorize_flag:
                    if value1 == 0:
                        json['username'] = message.text
                        value1 += 1
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.insert(types.InlineKeyboardButton(text='Да', callback_data='authorize'))
                        keyboard.insert(types.InlineKeyboardButton(text='Нет', callback_data='no'))
                        await message.answer('Вы уверены?', reply_markup=keyboard)
                    else:
                        json['password'] = message.text
                        authorize_flag = False
                        response = requests.get(f'http://127.0.0.1:5000/staff_api/authorize/{json["username"]}/'
                                                f'{json["password"]}')
                        if response:
                            response = response.json()
                            if response['success']:
                                keyboard = types.InlineKeyboardMarkup()
                                keyboard.insert(types.InlineKeyboardButton(text='Да', callback_data='search'))
                                keyboard.insert(types.InlineKeyboardButton(text='Нет', callback_data='ok'))
                                await message.answer('Хотите кого-то найти?', reply_markup=keyboard)
                            else:
                                keyboard = types.InlineKeyboardMarkup()
                                keyboard.add(types.InlineKeyboardButton(text='Зарегестрироваться',
                                                                        callback_data='common'))
                                keyboard.add(types.InlineKeyboardButton(text='Попробовать ещё раз',
                                                                        callback_data='authorize'))
                                await message.answer('Неверно введён юзернейм или пароль')
                                await message.answer("Хотите попробовать ещё раз или всё таки зарегестрируетесь?",
                                                     reply_markup=keyboard)
                        else:
                            await message.answer('Извините, произошла ошибка')
                            await message.answer(f'Http статус: {response.status_code} ({response.reason})')
                else:
                    if len(db_values) == 0:
                        if ' ' in message.text:
                            db_values.append(message.text)
                        else:
                            await message.answer('Некорректно введены имя и фамилия')
                    else:
                        if message.text.isdigit():
                            db_values.append(int(message.text))
                        else:
                            db_values.append(message.text)
                    if not photo_flag:
                        await next1(message)
                    else:
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='end_register'))
                        keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='update_blank'))
                        await message.answer('Отлично', reply_markup=types.ReplyKeyboardRemove())
                        await message.answer('Закончим регистрацию?', reply_markup=keyboard)


@dp.callback_query_handler(text='no')
async def no(call: types.CallbackQuery):
    global value1
    value1 = 0
    await authorize(call)


async def next1(message: types.Message):
    global ind, count_values, db_values
    if stop:
        await message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        if len(db_values) == 0:
            await begin(message)
        else:
            if count_values == len(db_values):
                ind += 1
                await register_asks_message(message)
                count_values += 1
            else:
                await message.answer('Вы ещё не ответили на прошлый вопрос')


@dp.callback_query_handler(text='next_data')
async def next_data(call: types.CallbackQuery):
    if stop:
        await call.message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        if len(db_values) == 0:
            await begin(call.message)
        else:
            await call.message.answer('OK')
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='end_register'))
            keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='update_blank'))
            await call.message.answer('Отлично', reply_markup=types.ReplyKeyboardRemove())
            await call.message.answer('Закончим регистрацию?', reply_markup=keyboard)


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    global update_flag, last_username, photo_flag
    if stop:
        await message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        await message.answer(await message.photo[-1].download(f'\\photos\\{message.chat.id}.jpg'))
        await message.answer('Ваше фото успешно сохранено.')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='update_blank'))
        keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='end_register'))
        if update_flag:
            await message.answer('Хотите ещё что-нибудь изменить?', reply_markup=keyboard)
        else:
            await message.answer('Хотите изменить анкету?', reply_markup=keyboard)


@dp.message_handler(content_types=['file'])
async def files(message: types.Message):
    if stop:
        await message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        await message.answer('Извините, я очень боюсь файловых бомб >-<')


async def register_asks_message(message: types.Message):
    global asks, ind, stop
    if stop:
        await message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
    else:
        telegram_values = [message.from_user.first_name + " " + message.from_user.last_name, 'Мужчина',
                           message.from_user.username, '', '', '']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if ind <= 2:
            if len(telegram_values[ind]) != 0:
                keyboard.add(types.KeyboardButton(text=f'{telegram_values[ind]}'))
            else:
                await message.answer('Упс... Похоже у вас скрыт юзернейм. Откройте его и перезапустите бота')
                stop = True
        if ind == 1:
            keyboard.add(types.KeyboardButton(text='Женщина'))
        if ind < len(asks):
            if ind <= 2:
                await message.answer(f'Укажите {asks[ind]}', reply_markup=keyboard)
            else:
                await message.answer(f'Укажите {asks[ind]}', reply_markup=types.ReplyKeyboardRemove())
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='update_blank'))
            keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='end_register'))
            await message.answer('Хотите изменить анкету?', reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)

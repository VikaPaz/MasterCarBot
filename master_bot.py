from telebot import TeleBot, types
import json


TOKEN = '6971909537:AAGbRyjyE2WfLqLpBxZobDuLCo8iSjM21BY'
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Войти в систему', callback_data='sign_in'))
    bot.send_message(chat_id, '🔐 <b>Войти</b> в систему для <u>старта</u>.', reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['main_menu'])
def main_message(message):
    chat_id = message.chat.id

    if not is_sign_in(chat_id):
        start_message(message)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Зарегистрировать авто', callback_data='car_reg'))
        bot.send_message(chat_id, 'main menu message.', reply_markup=markup)


def del_user_log(chat_id):
    if is_sign_in(chat_id):
        with open("sign_in_users.json", "r") as json_file:
            data = json.load(json_file)

        chat_id = str(chat_id)

        # Находим запись, которую нужно удалить (например, по ключу)
        if chat_id in data:
            del data[chat_id]

        # Сохраняем обновленные данные в файл
        with open("sign_in_users.json", "w") as json_file:
            json.dump(data, json_file)


@bot.message_handler(commands=['sign_out'])
def out_message(message):
        chat_id = message.chat.id

        if is_sign_in(chat_id):
            del_user_log(chat_id)
            bot.send_message(chat_id,  "🚪 <b>Сессия завершена.</b>\n", parse_mode='html')
            

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    call_funk = callback.data
    message = callback.message

    match call_funk:
        case 'sign_in':
            sign_in(message)
        case 'car_reg':
            car_registration(message)
        case 'exit_reg':
            exit_registration(message)
        case 'add_device':
            add_device(message)
        case 'add_name':
            add_name(message) 
        case 'add_gosnum':
            add_gosnum(message)   
        case 'add_brand':
            add_brand(message)
        case 'add_weels':
            add_weels(message)
        case 'add_brandWs':
            add_brandWs(message)
            


# Функция для проверки, зарегистрирован ли пользователь
def is_registered(login):
    with open('registered_users.json', 'r') as file:
        registered_users = json.load(file)
        return str(login) in registered_users.keys()
    

def is_acreditation(login, passwd):
    with open('registered_users.json', 'r') as file:
        registered_users = json.load(file)
        return passwd == registered_users[login]
    
def is_sign_in(chat_id):
    with open('sign_in_users.json', 'r') as file:
        registered_users = json.load(file)
        return str(chat_id) in list(registered_users.keys())

def add_user_log(chat_id, login):
    if not is_sign_in(chat_id):
        with open('sign_in_users.json', 'r') as file:
            registered_users = json.load(file)

        registered_users[chat_id] = str(login)

        with open('sign_in_users.json', 'w') as file:
            json.dump(registered_users, file)
    

def get_passwd(message, login):
    chat_id = message.chat.id

    passwd = message.text
    if is_acreditation(login, passwd):
        bot.send_message(chat_id,  "✅ <b>Вход</b> в систему <u>выполнен.</u>\n", parse_mode='html')
        add_user_log(chat_id, login)
        main_message(message)
    elif passwd == '/start': # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    elif passwd == '/sign_out':
        out_message(message)
    else:
        bot.send_message(chat_id, "🚫 <b>Неверный</b> <u>пароль.</u> \nПовторите попытку.\n", parse_mode='html')
        bot.register_next_step_handler(message,  get_passwd, login=login)


# Функция для регистрации пользователя
def get_login(message):
    chat_id = message.chat.id
    login = message.text

    if is_registered(login):
        bot.send_message(chat_id, "🔑 <b>Логин</b> есть <u>в системе.</u> \nВведите пароль.\n", parse_mode='html')
        bot.register_next_step_handler(message,  get_passwd, login=login)
    elif login == '/start': # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    else:
        bot.send_message(chat_id, "🚫 <b>Логин</b> <u>не зарегистрирован</u> в системе. \nПовторите попытку.\n", parse_mode='html')
        bot.register_next_step_handler(message,  get_login)


def sign_in(message):
    chat_id = message.chat.id

    if not is_sign_in(chat_id):
        bot.send_message(chat_id,  "💼 <b>Введите</b> логин компании.", parse_mode='html')
        bot.register_next_step_handler(message,  get_login)
    else: 
        main_message(message)


def car_registration(message, **kwags):
    chat_id = message.chat.id

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🚫', callback_data='exit_reg'))
    bot.send_message(chat_id, '❗   ❗   Завершить регистрацию.  ❗  ❗', reply_markup=markup)
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('⚙️ Устройство', callback_data='add_device')
    btn2 = types.InlineKeyboardButton('🏢 Компания', callback_data='add_name')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('🚘 Государственный номер', callback_data='add_gosnum')
    btn4 = types.InlineKeyboardButton('🚗 Марка автомобиля', callback_data='add_brand')
    markup.row(btn3, btn4)
    btn5 = types.InlineKeyboardButton('🛞 Количество колес', callback_data='add_weels')
    btn6 = types.InlineKeyboardButton('🔄 Марка шин', callback_data='add_brandWs')
    markup.row(btn5, btn6)
    markup.add(types.InlineKeyboardButton('✅', callback_data='end_reg'))
    if not kwags:
        bot.send_message(chat_id,  f"⚙️ <b>Добавление <u>устройств</u> в базу данных</b> \n🆔 <b>Укажите</b> <u>ID</u> устройства\n🏢 <b>Введите</b> <u>наименование компании</u>\n🚗 <b>Введите</b> государственный <u>номер автомобиля</u>\n🚘 <b>Укажите</b> <u>марку автомобиля</u>\n🛞 <b>Введите</b> количество <u>колёс</u> автомобиля\n🔄 <b>Укажите</b> <u>марку шин</u>\n", parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(chat_id,  f"⚙️ <b>Добавление <u>устройств</u> в базу данных</b> \n🆔 <b>{kwags['device']}</b> <u>ID</u> устройства\n🏢 <b>Введите</b> <u>наименование компании</u>\n🚗 <b>Введите</b> государственный <u>номер автомобиля</u>\n🚘 <b>Укажите</b> <u>марку автомобиля</u>\n🛞 <b>Введите</b> количество <u>колёс</u> автомобиля\n🔄 <b>Укажите</b> <u>марку шин</u>\n", parse_mode='html', reply_markup=markup)

    

def exit_registration(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, 'Регистрация завершена.')
    main_message(message)

def add_device(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🆔 <b>Укажите</b> <u>ID</u> устройства', parse_mode='html')
    bot.register_next_step_handler(message, device_property)

def add_name(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🏢 <b>Введите</b> <u>наименование компании</u>', parse_mode='html')
    bot.register_next_step_handler(message, name_property)

def add_gosnum(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🚗 <b>Введите</b> государственный <u>номер автомобиля</u>', parse_mode='html')

def add_brand(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🚘 <b>Укажите</b> <u>марку автомобиля</u>', parse_mode='html')

def add_weels(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🛞 <b>Введите</b> количество <u>колёс</u> автомобиля', parse_mode='html')

def add_brandWs(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, '🔄 <b>Укажите</b> <u>марку шин</u>', parse_mode='html')

def device_property(message):
    chat_id = message.chat.id

    device = message.text
    bot.send_message(chat_id, f'Девайс {device} добавлен')
    car_registration(message, device=device)

def name_property(message):
    pass

def gosnum_property(message):
    pass

def brand_property(message):
    pass

def weels_property(message):
    pass

def brandWs_property(message):
    pass



bot.infinity_polling()
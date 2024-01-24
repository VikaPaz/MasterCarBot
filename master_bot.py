from telebot import TeleBot, types
from acreditation import get_key 
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
def main_message(message, is_sign_in: bool=False):
    chat_id = message.chat.id

    if not is_sign_in:
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
            bot.send_message(chat_id, 'Сессия завершина.')
            

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
        bot.send_message(chat_id, 'Вход в систему выполнен.')
        add_user_log(chat_id, login)
        main_message(message, is_sign_in=True)
    elif passwd == '/start': # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message) 
    else:
        bot.send_message(chat_id, 'Неверный пароль. \nПовторите попытку.')
        bot.register_next_step_handler(message,  get_passwd, login=login)


# Функция для регистрации пользователя
def get_login(message):
    chat_id = message.chat.id
    login = message.text

    if is_registered(login):
        bot.send_message(chat_id, 'Логин есть в системе.\nВведите пароль.')
        bot.register_next_step_handler(message,  get_passwd, login=login)
    elif login == '/start': # for break from menu, do you think that we should add InlineKeyboardButton?
        start_message(message)
    else:
        bot.send_message(chat_id, 'Логин не зарегистрировани в системе. \nПовторите попытку.')
        bot.register_next_step_handler(message,  get_login)


def sign_in(message):
    chat_id = message.chat.id

    if not is_sign_in(chat_id):
        bot.send_message(chat_id, 'Введите логин компании.')
        bot.register_next_step_handler(message,  get_login)


def car_registration(message):
    pass



bot.infinity_polling()
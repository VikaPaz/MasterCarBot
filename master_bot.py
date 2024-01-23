from telebot import TeleBot, types
from acreditation import get_key 
import json


TOKEN = '6971909537:AAGbRyjyE2WfLqLpBxZobDuLCo8iSjM21BY'
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Вход в систему', callback_data='sign_in'))
    bot.send_message(chat_id, 'Войти в систему для старта', reply_markup=markup)
    
    # markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton('Вход в систему', callback_data=''))
    # bot.send_message(chat_id, 'Войти в систему для старта', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    if callback.data == 'sign_in':
        sign_in(callback.message)


# Функция для проверки, зарегистрирован ли пользователь
def is_registered(login):
    with open('registered_users.json', 'r') as file:
        registered_users = json.load(file)
        return str(login) in registered_users.keys()
    

def acreditation(login, passwd):
    with open('registered_users.json', 'r') as file:
        registered_users = json.load(file)
        return passwd == registered_users[login]
    

def get_passwd(message, login):
    chat_id = message.chat.id

    passwd = message.text
    if acreditation(login, passwd):
        bot.send_message(chat_id, 'Вход в систему выполнен.')
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
    else:
        bot.send_message(chat_id, 'Логин не зарегистрировани в системе. \nПовторите попытку.')
        bot.register_next_step_handler(message,  get_login)


def sign_in(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введите логин компании.')
    bot.register_next_step_handler(message,  get_login)




bot.infinity_polling()
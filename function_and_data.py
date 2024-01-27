# Тут я решил оставить все функции и переменную, которые не уникальны

from telebot import TeleBot
import json

TOKEN = '6971909537:AAGbRyjyE2WfLqLpBxZobDuLCo8iSjM21BY'
bot = TeleBot(TOKEN)

message_id = {0: [0, 0]}


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


# Функция для удаления сообщений
def del_message(chat_id):
    print(message_id[chat_id])
    for i in message_id[chat_id]:
        try:
            bot.delete_message(chat_id, i)
        except Exception as e:
            print(e)
    message_id[chat_id].clear()


# Функция для добавления сообщений в список для удаления
def add_message(message):
    if message.chat.id not in message_id:
        message_id[message.chat.id] = []
    message_id[message.chat.id].append(message.id)


# Функция для отправки сообщения
def send_message(chat_id, message, **kwargs):
    m = bot.send_message(chat_id, message, **kwargs)
    add_message(m)

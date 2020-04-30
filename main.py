import os, telebot, logging, sys
from flask import Flask, request
from asyncio import run
from Classes.SCPFoundationAPI import SCPFoundationAPI
from Classes.Main import SQLMain
from Classes.Core.Debug import Debug

# scpAPI = SCPFoundationAPI()
# print(scpAPI.GetObjectByNumber("3333"))

# sql = SQLMain()
# sql.SetFavoriteByChatID(666314796, "3333")
# print(sql.GetFavoriteFromChatID(666314796))
# sql.SetSourceFromChatID(666314796, "ENG")
# print(sql.GetSourceFromChatID(666314796))


TOKEN = os.environ.get('TOKEN')

if (not TOKEN): sys.exit()

bot = telebot.TeleBot(TOKEN)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "Saves/SCPBot.db")
sql = SQLMain()
print(sql.GetAllTables())

@bot.message_handler(commands=['start'])
def start_message(message):
    Debug.Message(Debug, object=f"chat_id={message.chat.id}")
    bot.send_message(message.chat.id, f"Введите номер объекта...\n\nПредупреждение: Telegram не позволяет отправлять сообщения содержащие более 4096 символов, поэтому сообщение может делиться на несколько.")

@bot.message_handler(commands=['favorite'])
def send_FavoriteList(message):
    temp_list = sql.GetFavoriteFromChatID(message.chat.id)
    if (len(temp_list) > 1): temp_list = temp_list[1:]
    Debug.Message(Debug, object=f"chat_id={message.chat.id}; temp_list={temp_list}")
    for i in temp_list:
        if (i == "None"): bot.send_message(message.chat.id, f"{i}")
        else:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(text="Удалить.", callback_data=f"d_{i}"))
            bot.send_message(message.chat.id, f"{i}", reply_markup=keyboard)

@bot.message_handler(commands=['source'])
def send_SettingSource(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in sql.GetAllSources():
        key = telebot.types.InlineKeyboardButton(text=i, callback_data=f"s_{i}")
        keyboard.add(key)
    Debug.Message(Debug, object=f"chat_id={message.chat.id}")
    bot.send_message(message.chat.id, f"Выберете источник поиска: ", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_scpText(message):
    Debug.Warning(Debug, object=f"Get message: chat_id={message.chat.id}, message_id={message.message_id}")

    if (len(message.text) > 10):
        bot.send_message(message.chat.id, "Слишком большое сообщение.")
        return

    url = None
    try: url = sql.GetSourceFromChatID(message.chat.id)
    except TypeError: print("Person has NoneType")

    for i in range(3): bot.send_message(message.chat.id, "Внимание! Дальше следует секретная информация.")

    keyboard = telebot.types.InlineKeyboardMarkup()
    add_Key = telebot.types.InlineKeyboardButton(text="Добавить.", callback_data=f"a_{message.text}")
    keyboard.add(add_Key)
    del_Key = telebot.types.InlineKeyboardButton(text="Удалить.", callback_data=f"d_{message.text}")
    keyboard.add(del_Key)

    scpStrings = run(SCPFoundationAPI.GetObjectByNumber(SCPFoundationAPI, message.text, url=url))
    for i in range(len(scpStrings)):
        if (i == len(scpStrings) - 1):
            bot.send_message(message.chat.id, scpStrings[i], reply_markup=keyboard)
            continue
        bot.send_message(message.chat.id, scpStrings[i])

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    data, prefix = call.data[2:], call.data[:1]
    Debug.Message(Debug, object=f"Data = {data}; Prefix = {prefix};")

    if (prefix == "s"):
        person = sql.GetUserFromChatID(call.message.chat.id)
        if (person):
            Debug.Success(Debug, object=f"Person was found in database!")
            sql.SetSourceFromChatID(call.message.chat.id, data)
        else:
            Debug.Error(Debug, object=f"Person was not found in database, start create a new user!")
            sql.SetUserFromChatID(call.message.chat.id)
            sql.SetSourceFromChatID(call.message.chat.id, data)

        Debug.Success(Debug, object="Settings was saved!")
        bot.send_message(call.message.chat.id, f"Настройки сохранены.")

    elif (prefix == "a"):
        person = sql.GetUserFromChatID(call.message.chat.id)
        if (person):
            Debug.Success(Debug, object=f"Person was found in database!")
            sql.SetFavoriteByChatID(call.message.chat.id, data)
        else:
            Debug.Error(Debug, object=f"Person was not found in database, start create a new user!")
            sql.SetUserFromChatID(call.message.chat.id)
            sql.SetFavoriteByChatID(call.message.chat.id, data)

        Debug.Success(Debug, object="Complete!")
        bot.send_message(call.message.chat.id, f"Успешно.")

    elif (prefix == "d"):
        person = sql.GetUserFromChatID(call.message.chat.id)
        if (person):
            Debug.Success(Debug, object=f"Person was found in database!")
            sql.RemoveFavoriteByChatID(call.message.chat.id, data)
        else:
            Debug.Error(Debug, object=f"Person was not found in database, start create a new user!")
            sql.SetUserFromChatID(call.message.chat.id)
            sql.RemoveFavoriteByChatID(call.message.chat.id, data)

        Debug.Success(Debug, object="Complete!")
        bot.send_message(call.message.chat.id, f"Успешно.")


if ("HEROKU" in list(os.environ.keys())):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    bot.remove_webhook()
    bot.set_webhook(url="https://bot-farm-telegram-game.herokuapp.com/bot")  # этот url нужно заменить на url вашего Хероку приложения

    server = Flask(__name__)

    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
import os, telebot, logging, sys
from flask import Flask, request
from asyncio import run
from Classes.SCPFoundationAPI import SCPFoundationAPI
from Classes.Main import Main
from Classes.Main import SQLMain

# scpAPI = SCPFoundationAPI()
# print(scpAPI.GetObjectByNumber("3333"))


"""
sql = SQLMain()
sql.SetFavoriteByChatID(666314796, "3333")
print(sql.GetFavoriteFromChatID(666314796))
print(sql.SetSourceFromChatID(666314796, "RU"))
"""

TOKEN = os.environ.get('TOKEN')

if (not TOKEN): sys.exit()

bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Saves/SCPBot.db")
sql = SQLMain(db_path)
print(sql.GetAllSources())

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Введите номер объекта...\n\nПредупреждение: Telegram не позволяет отправлять сообщения содержащие более 4096 символов, поэтому сообщение может делиться на несколько.")

@bot.message_handler(commands=['source'])
def send_SettingSource(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in sql.GetAllSources():
        key = telebot.types.InlineKeyboardButton(text=i, callback_data=f"s_{i}")
        keyboard.add(key)
    bot.send_message(message.chat.id, f"Выберете источник поиска: ", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_scpText(message):
    url = None
    try: url = sql.GetSourceFromChatID(message.chat.id)
    except TypeError: print("Person has NoneType")

    for i in range(3): bot.send_message(message.chat.id, "Внимание! Дальше следует секретная информация.")

    scpStrings = run(SCPFoundationAPI.GetObjectByNumber(SCPFoundationAPI, message.text, url=url))
    for scpString in scpStrings:
        bot.send_message(message.chat.id, scpString)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    data, prefix = call.data[2:], call.data[:1]
    print(f"Data = {data}; Prefix = {prefix};")

    if (prefix == "s"):
        person = sql.GetUserFromChatID(1)
        if (person): sql.SetSourceFromChatID(call.message.chat.id, data)
        else:
            sql.SetUserFromChatID(call.message.chat.id)
            sql.SetSourceFromChatID(call.message.chat.id, data)

    bot.send_message(call.message.chat.id, f"Настройки сохранены.")


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
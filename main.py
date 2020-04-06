import os, telebot, logging, sys
from flask import Flask, request
from asyncio import run
from Classes.SCPFoundationAPI import SCPFoundationAPI
from Classes.Main import Main

# scpAPI = SCPFoundationAPI()
# print(scpAPI.GetObjectByNumber("3333"))

TOKEN = os.environ.get('TOKEN')

if (not TOKEN): sys.exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Введите номер объекта...\n\nПредупреждение: Telegram не позволяет отправлять сообщения содержащие более 4096 символов, поэтому сообщение может делиться на несколько.")

@bot.message_handler(commands=['settingSource'])
def send_SettingSource(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in SCPFoundationAPI.urls:
        key = telebot.types.InlineKeyboardButton(text=i, callback_data=f"s_{i}")
        keyboard.add(key)
    bot.send_message(message.chat.id, f"Выберете источник поиска: ", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_scpText(message):
    url = None
    try: url = Main.LoadPerson(Main, message.chat.id)["url"]
    except TypeError: print("Person has NoneType")

    scpStrings = run(SCPFoundationAPI.GetObjectByNumber(SCPFoundationAPI, message.text, url=url))
    for scpString in scpStrings:
        bot.send_message(message.chat.id, scpString)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    data, prefix = call.data[2:], call.data[:1]
    print(f"Data = {data}; Prefix = {prefix};")

    if (prefix == "s"):
        personDictionary = Main.LoadPerson(Main, call.message.chat.id)
        if (personDictionary): Main.SavePerson(Main, chat_id=personDictionary["chat_id"], newUrl=data)
        else: Main.SavePerson(Main, chat_id=call.message.chat.id, newUrl=data)

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

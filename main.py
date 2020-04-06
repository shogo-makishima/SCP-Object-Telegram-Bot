import os, telebot, logging, sys
from flask import Flask, request
from asyncio import run
from Classes.SCPFoundationAPI import SCPFoundationAPI

# scpAPI = SCPFoundationAPI()
# print(scpAPI.GetObjectByNumber("3333"))

TOKEN = os.environ.get('TOKEN')

if (not TOKEN): sys.exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Введите номер объекта...")

@bot.message_handler(content_types=['text'])
def send_text(message):
    scpText = run(SCPFoundationAPI.GetObjectByNumber(SCPFoundationAPI, "3333"))
    bot.send_message(message.chat.id, scpText)

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

import os, telebot, logging, sys
from flask import Flask, request
from asyncio import run
from Classes.SCPFoundationAPI import SCPFoundationAPI
from Classes.Main import SQLMain
from Classes.Core.Debug import Debug
from Classes.CurrencyAPI import CurrencyAPI
from Classes.WeatherAPI import WeatherAPI

TOKEN = os.environ.get('TOKEN')

if (not TOKEN): sys.exit()

bot = telebot.TeleBot(TOKEN)

sql = SQLMain()
currency = CurrencyAPI()
weather = WeatherAPI()
print(sql.GetAllTables())

def CheckRegisterUser(chat_id: int):
    person = sql.GetUserFromChatID(chat_id)
    return person is not None

def CheckSpecialFuncitons(chat_id: int):
    person = sql.GetUserFromChatID(chat_id)
    if (person is None): return False
    else: return not person[-1]

def ExtractArgs(args):
    return args.split()[1:]

def IsFloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

@bot.message_handler(commands=['start'])
def start_message(message):
    Debug.Message(Debug, object=f"chat_id={message.chat.id}")
    bot.send_message(message.chat.id, f"Введите номер объекта...\n\nПредупреждение: Telegram не позволяет отправлять сообщения содержащие более 4096 символов, поэтому сообщение может делиться на несколько.")

@bot.message_handler(commands=["currency"])
def send_currency(message):
    if (CheckSpecialFuncitons(message.chat.id)): bot.send_message(message.chat.id, f"Доступ запрещён!"); return
    args = ExtractArgs(message.text)

    try:
        if (len(args) == 1):
            temp_list = sql.GetCurrencyFromCodeName(args[0])
            bot.send_message(message.chat.id, f"{temp_list[1]}: {temp_list[2]} {temp_list[3]} -> {temp_list[4]}")
        else:
            Debug.Message(Debug, object=f"chat_id={message.chat.id}")
            temp_list = run(currency.Update())
            Debug.Message(Debug, object=f"chat_id={message.chat.id}; temp_list={temp_list}")

            keyboard = telebot.types.InlineKeyboardMarkup()
            temp_message = bot.send_message(message.chat.id, f"Валюты", reply_markup=keyboard)
            for i in temp_list:
                keyboard.add(telebot.types.InlineKeyboardButton(text=f"{i.code_name}", callback_data=f"c^{i.code_name}^{temp_message.message_id}"))
            bot.edit_message_text(text=temp_message.text, chat_id=temp_message.chat.id, message_id=temp_message.message_id, reply_markup=keyboard)
    except Exception as exception:
        Debug.Error(Debug, exception)
        bot.send_message(message.chat.id, "Данные не валидны")

@bot.message_handler(commands=["update_currency"])
def send_currencyUpdate(message):
    if (CheckSpecialFuncitons(message.chat.id)): bot.send_message(message.chat.id, f"Доступ запрещён!"); return
    sql.UpdateCurrencyFromList(run(currency.Update()))
    bot.send_message(message.chat.id, "Успешно")

@bot.message_handler(commands=["current_chat_id"])
def send_CurrecntChatId(message):
    if (CheckSpecialFuncitons(message.chat.id)): bot.send_message(message.chat.id, f"Доступ запрещён!"); return
    bot.send_message(message.chat.id, f"chat_id: {message.chat.id}")

@bot.message_handler(commands=["special_commands"])
def send_specialCommandsList(message):
    if (CheckSpecialFuncitons(message.chat.id)): bot.send_message(message.chat.id, f"Доступ запрещён!"); return
    bot.send_message(message.chat.id, f"Специальные команды:\n-> /currency - Список валют (Или например: /currency USD)\n-> /update_currency - Обновить курс валют\n-> /weather - Погода\n-> /current_chat_id - Текущий chat_id")

@bot.message_handler(commands=["weather"])
def send_weather(message, *args):
    if (CheckSpecialFuncitons(message.chat.id)): bot.send_message(message.chat.id, f"Доступ запрещён!"); return
    print(*args)

    args = ExtractArgs(message.text)
    Debug.Message(Debug, args)
    try:
        if (len(args) == 0):
            bot.send_message(message.chat.id, "Отправь мне свою геолокацию или:\n-> Напиши команду /weather <lat> <lon> (Например: /weather 54.55493 36.329075)\n-> Напиши команду /weather <lat> <lon> <count> (Например: /weather 54.55493 36.329075 10)\n-> Напиши команду /weather <city> (Например: /weather Калуга)\n-> Напиши команду /weather <city> <count> (Например: /weather Калуга 10)\n\n-> P.S. Если название города содержит несколько слов, то используйте вместо пробела символ '+'.")
        elif (len(args) == 1):
            bot.send_message(message.chat.id, weather.GetWeatherByCityName(args[0].replace("+", " ")))
        elif (len(args) == 2):
            if (IsFloat(args[0]) and IsFloat(args[1])):
                bot.send_message(message.chat.id, weather.GetWeatherByPosition(float(args[0]), float(args[1])))
            if (args[0] and args[1].isdigit()):
                temp_list = weather.GetForecastWeatherByCityName(args[0].replace("+", " "), int(args[1]))
                for element in temp_list: bot.send_message(message.chat.id, element)
        elif (len(args) == 3):
            temp_list = weather.GetForecastWeatherByPosition(float(args[0]), float(args[1]), int(args[2]))
            for element in temp_list: bot.send_message(message.chat.id, element)
        else: bot.send_message(message.chat.id, "Данные не валидны")
    except Exception as exception:
        Debug.Error(Debug, exception)
        bot.send_message(message.chat.id, "Данные не валидны")

@bot.message_handler(content_types=["location"])
def get_location(message):
    if (CheckSpecialFuncitons(message.chat.id)): bot.send_message(message.chat.id, f"Доступ запрещён!"); return
    if (message.location is not None):
        bot.send_message(message.chat.id, weather.GetWeatherByPosition(message.location.latitude, message.location.longitude))
        Debug.Success(Debug, "latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))

@bot.message_handler(commands=['favorite'])
def send_FavoriteList(message):
    temp_list = sql.GetFavoriteFromChatID(message.chat.id)
    if (len(temp_list) > 1): temp_list = temp_list[1:]
    Debug.Message(Debug, object=f"chat_id={message.chat.id}; temp_list={temp_list}")
    for i in temp_list:
        if (i == "None"): bot.send_message(message.chat.id, f"{i}")
        else:
            keyboard = telebot.types.InlineKeyboardMarkup()
            temp_message = bot.send_message(message.chat.id, f"{i}", reply_markup=keyboard)
            keyboard.add(telebot.types.InlineKeyboardButton(text="Удалить.", callback_data=f"d^{i}^{temp_message.message_id}"))
            bot.edit_message_text(text=temp_message.text, chat_id=temp_message.chat.id, message_id=temp_message.message_id, reply_markup=keyboard)
            Debug.Warning(Debug, object=f"{temp_message.message_id}")

@bot.message_handler(commands=['source'])
def send_SettingSource(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in sql.GetAllSources():
        key = telebot.types.InlineKeyboardButton(text=i, callback_data=f"s^{i}^n")
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
    keyboard.add(telebot.types.InlineKeyboardButton(text="Добавить.", callback_data=f"a^{message.text}^n"))

    scpStrings = run(SCPFoundationAPI.GetObjectByNumber(SCPFoundationAPI, message.text, url=url))
    for i in range(len(scpStrings)):
        if (i == len(scpStrings) - 1):
            bot.send_message(message.chat.id, scpStrings[i], reply_markup=keyboard)
            continue
        bot.send_message(message.chat.id, scpStrings[i])

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    temp_data = call.data.split("^")
    try: prefix, data, postfix = temp_data[0], temp_data[1], temp_data[2]
    except Exception as exception:
        Debug.Error(Debug, f"exception={exception}, temp_data={temp_data}")
        return

    Debug.Message(Debug, object=f"prefix = {prefix}; data = {data}; postfix = {postfix};")
    
    if (prefix == "s"):
        if (CheckRegisterUser(call.message.chat.id)):
            Debug.Success(Debug, object=f"Person was found in database!")
            sql.SetSourceFromChatID(call.message.chat.id, data)
        else:
            Debug.Error(Debug, object=f"Person was not found in database, start create a new user!")
            sql.SetUserFromChatID(call.message.chat.id)
            sql.SetSourceFromChatID(call.message.chat.id, data)

        Debug.Success(Debug, object="Settings was saved!")
        bot.send_message(call.message.chat.id, f"Настройки сохранены.")

    elif (prefix == "a"):
        if (CheckRegisterUser(call.message.chat.id)):
            Debug.Success(Debug, object=f"Person was found in database!")
            sql.SetFavoriteByChatID(call.message.chat.id, data)
        else:
            Debug.Error(Debug, object=f"Person was not found in database, start create a new user!")
            sql.SetUserFromChatID(call.message.chat.id)
            sql.SetFavoriteByChatID(call.message.chat.id, data)

        Debug.Success(Debug, object="Add was completed!")

    elif (prefix == "d"):
        if (CheckRegisterUser(call.message.chat.id)):
            Debug.Success(Debug, object=f"Person was found in database!")
            sql.RemoveFavoriteByChatID(call.message.chat.id, data)
            bot.delete_message(chat_id=call.message.chat.id, message_id=postfix)
        else:
            Debug.Error(Debug, object=f"Person was not found in database, start create a new user!")
            sql.SetUserFromChatID(call.message.chat.id)
            sql.RemoveFavoriteByChatID(call.message.chat.id, data)
            bot.delete_message(chat_id=call.message.chat.id, message_id=postfix)

        Debug.Success(Debug, object="Delete was completed!")

    elif (prefix == "c"):
        temp_list = sql.GetCurrencyFromCodeName(data)
        Debug.Message(Debug, object=temp_list)
        bot.send_message(call.message.chat.id, f"{temp_list[1]}: {temp_list[2]} {temp_list[3]} -> {temp_list[4]}")
        bot.delete_message(chat_id=call.message.chat.id, message_id=postfix)

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
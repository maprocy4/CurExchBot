#!/usr/bin/python

import telebot
from config import curs, TOKEN
from extensions import APIException, CurConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду боту в следующем формате:\n<название валюты, которую вы хотите перевести>\
<название валюты перевода> <количество переводимой валюты>.\n\
\n\
Увидеть список доступных валют: /curs."
    bot.reply_to(message, text)

@bot.message_handler(commands=["curs"])
def view_curs(message: telebot.types.Message):
    text = "Доступные валюты:\n\
RUB - Российский рубль;\n\
USD - Доллар США;\n\
EUR - Евро."
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIException("Неверное количество параметров.")

        quote, base, amount = values

        total_base = CurConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"{amount} {quote} в {base} = {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

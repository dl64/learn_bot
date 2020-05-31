import settings
import logging
import ephem

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters # CommandHandler регирует только на команды, MessageHandler широкий обработчик, реагирует на любые сообщения. Библиотека filters помогает фильтровать MessageHandler'у только текстовые сообщения
from datetime import datetime

logging.basicConfig(filename="botmars.log", level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context): # update - то, что пришло из ТГ и много сервисной информации из ТГ, а через context отдаем команды боту
    print("Вызван /start") # вернул в консоль
    update.message.reply_text("Здравствуй, пользователь!") # ответить пользователю в ТГ

def planet_finder(update, context):
    planet_from_inquiry = update.message.text.split()[1]
    planet = getattr(ephem, planet_from_inquiry)
    planet = planet(datetime.now())
    constellation = ephem.constellation(planet)[1]
    update.message.reply_text(constellation)

def talk_to_me(update,context):
    text = update.message.text # полученный текст хранится в update.message.text
    print(text) # в консоль
    update.message.reply_text('А бот отвечает: ' + text[::-1]) # отправим пользователю в ответ его текст наоборот

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY) # авторизуется и запрашивает ТГ через PROXY
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user)) #без косой черточки, слэш записан в библиотеке у авторов. add_handler проверил, что у обработчика зарегистрировано действие на команду start - вызвать функцию Greet_User
    dp.add_handler(CommandHandler("planet", planet_finder))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # MessageHandler ставить ниже CommandHandler, чтобы команды дошли до CommandHandler'a, иначе их перехватит MessageHandler.
    # будет реагировать только на текстовые сообщения. вызывает функцию talk_to_me

    logging.info("bot started")
    mybot.start_polling() # постоянные запросы в ТГ
    mybot.idle() # бесконечный цикл работы

if __name__ == "__main__":
    main()

from urllib.request import urlopen
import requests
import re
import json
import logging
from time import localtime, strftime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# f18f86869f5e61b09b9bda26d871c191 - OpenWeatherApiKey
# 6172963477:AAGRhUEgXw7KelJOMqYUDT1CmhQtqxqV9Jc - TelegramApi

# loggin
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# get weather
def get_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, API_KEY)
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    city = data['city']
    weather_data = get_weather(city)
    if weather_data ["cod"] == 200:
        temp = weather_data['main']['temp']
        message = 'Сейчас {}. \nТемпература в вашем городе {} сейчас {} градусов по Цельсию. \nВведите название города в котором хотите узнать погоду.'.format(strftime("%H:%M", localtime()), city, temp)
    else:
        message = 'Не удалось получить информацию о погоду в вашем городе. \nВведите название города, погоду которого хотите узнать.'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# /contacts
async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    keyboard = [
        [
            InlineKeyboardButton("Telegram", url='https://t.me/lunando'),
            InlineKeyboardButton("Instagram", url='https://www.instagram.com/blackword.ss/'),
            InlineKeyboardButton("GitHub", url='https://github.com/azerotick')
        ],  
        [InlineKeyboardButton("А что еще надо?", url='https://avatars.dzeninfra.ru/get-zen_doc/34175/pub_5cea2361585c2f00b5c9cb0b_5cea310a752e5b00b25b9c01/scale_1200')],
    ]
    contactkeys = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Контакты создателя бота:', reply_markup=contactkeys)

# /help
async def help (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Я бот помощник. Могу показать тебе погоду в любом городе мира. Пожалуйста, пиши правильное название города на русском или английском языке, и всё получится. Удачи, друг!')


# user message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = update.message.text
    weather_data = get_weather(city)
    if weather_data['cod'] == 200:
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        message = 'Сейчас {}.\nТемпература в городе {} сейчас {} градусов по Цельсию. {}'.format( strftime("%H:%M", localtime()),city, temp, description)
    else:
        message = 'Не удалось получить прогноз погоды для города {}. Попробуйте еще раз.'.format(city)     
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

#API-ключ для OpenWeatherMap
API_KEY = 'f18f86869f5e61b09b9bda26d871c191'

# bot build
application = Application.builder().token("6172963477:AAGRhUEgXw7KelJOMqYUDT1CmhQtqxqV9Jc").build()

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
contacts_hendler = CommandHandler('contacts', contacts)

application.add_handler(help_handler)
application.add_handler(start_handler)
application.add_handler(echo_handler)
application.add_handler(contacts_hendler)


application.run_polling()

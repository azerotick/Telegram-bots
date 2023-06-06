import logging
from urllib.request import urlopen
import requests
import json
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, __version__ as TG_VER

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
# 6172963477:AAGRhUEgXw7KelJOMqYUDT1CmhQtqxqV9Jc - TelegramApi

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

    

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    city = data ['city']
    country = data['country']
    IP = data['ip']
    await update.message.reply_text('Попался, я вычислил тебя по IP! \nТвой IP: {}\nТы тут: {}, {}.\nБерегись, я выехал!'.format(IP, country, city))

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

async def help (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Ты попался в мою ловушку!😈')

application = Application.builder().token("6172963477:AAGRhUEgXw7KelJOMqYUDT1CmhQtqxqV9Jc").build()

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
contacts_hendler = CommandHandler('contacts', contacts)

application.add_handler(help_handler)
application.add_handler(start_handler)
application.add_handler(contacts_hendler)


application.run_polling()
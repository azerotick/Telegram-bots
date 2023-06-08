import telebot
from telebot import types

token = '6172963477:AAGRhUEgXw7KelJOMqYUDT1CmhQtqxqV9Jc'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def hello(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(types.KeyboardButton('Telegram cоздателя')),  keyboard.add(types.KeyboardButton('Instargram cоздателя')),
    keyboard.add(types.KeyboardButton('GitHub cоздателя'))
    bot.send_message(message.chat.id, f'Hi {message.from_user.first_name}!', reply_markup=keyboard)

    bot.polling(none_stop=True)
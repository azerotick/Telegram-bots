import logging
import random
from telegram import __version__ as TG_VER
from telegram import Update, ForceReply
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, Application, ContextTypes

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

# Замени на свой токен, который ты получишь от BotFather
TOKEN = "6172963477:AAGRhUEgXw7KelJOMqYUDT1CmhQtqxqV9Jc"

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Задай мне вопрос, и я отвечу "Да" или "Нет".')

async def help (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Я бот помощник. МОгу показать тебе погоду в любом городе мира. Пожалуйста, пиши правильное название города на русском или английском языке, и всё получится. Удачи, друг!')

async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    responses = ["Да", "Нет"]
    await update.message.reply_text(random.choice(responses))

def main() -> None:
    # Create the Application and pass it your bot's token.
    dp = Application.builder().token("6172963477:AAGRhUEgXw7KelJOMqYUDT1CmhQtqxqV9Jc").build()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.TEXT& ~filters.COMMAND, answer_question))

    dp.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

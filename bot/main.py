from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot.handlers import start_command, text_router
from bot.config import settings


def main():
    updater = Updater(settings.BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text, text_router))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

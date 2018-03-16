from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import handlers
import conf


updater = Updater(token=conf.telegram_bot_token)

updater.dispatcher.add_handler(CommandHandler('start', handlers.start_command_callback))
updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.sticker, handlers.text_message_callback))


if __name__ == '__main__':
    updater.start_polling(clean=True)
    print('Ехала...')
    updater.idle()

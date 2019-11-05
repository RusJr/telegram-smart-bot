import logging

import telegram

from p_bot import PBotManager


logger = logging.getLogger('telegram-smart-bot')


def send_text(update, text):
    bot = update.message.bot
    bot.send_message(chat_id=update.message.chat_id, text=text)
    logger.info('[me] %s', text)


def text_message_callback(bot: telegram.Bot, update):
    if update.message.sticker:
        if update.message.sticker.file_id in ('CAADAgADTgIAAiHtuwPIk696OrWIhgI', 'CAADAgADMgIAAiHtuwO7d0YhJHL79AI'):
            bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker)
    else:
        recived_msg = update.message.text.strip()
        logger.info('[%s] %s', update.message.from_user.full_name, recived_msg)

        if recived_msg in ('хуй', 'пизда', 'хуйло', 'пидр', 'пидор', 'сука'):
            send_text(update, text='Сам такой))))0')
        else:
            p_bot = PBotManager.get_or_create(update.message.from_user.id, update.message.from_user.full_name)
            send_text(update, text=p_bot.get_answer(recived_msg))


def start_command_callback(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='дратути')

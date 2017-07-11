from jinny_spends_cfg import *
from jinny_spends_static import *
import logging
from logging.handlers import RotatingFileHandler

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, StringRegexHandler, jobqueue, CallbackQueryHandler)
from telegram import replykeyboardmarkup, inlinekeyboardbutton, inlinekeyboardmarkup
from telegram import replykeyboardremove

from functools import wraps

# decorator to restrict the use of the functions from unauthorized users
def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        # extract user_id from arbitrary update
        try:
            user_id = update.message.from_user.id
        except (NameError, AttributeError):
            try:
                user_id = update.inline_query.from_user.id
            except (NameError, AttributeError):
                try:
                    user_id = update.chosen_inline_result.from_user.id
                except (NameError, AttributeError):
                    try:
                        user_id = update.callback_query.from_user.id
                    except (NameError, AttributeError):
                        print("No user_id available in update.")
                        logging.info("No user_id available in update.")
                        return
        if user_id not in LIST_OF_ADMINS:
            logging.info(log_i_dont_know_u.format(user_id))
            bot.sendMessage(chat_id=update.message.chat_id, text=msg_i_dont_know_u)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

@restricted
def start(bot, update):
    markup = replykeyboardmarkup.ReplyKeyboardMarkup(keyboard=keyboard_start)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg_greeting,
                    reply_markup=markup)


def main():

    handler =  RotatingFileHandler(filename="logs/JinnyReminds.log", maxBytes=log_file_size_lmt, backupCount=log_file_count_lmt)
    handler.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))

    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()


if __name__ == '__main__':
    main()

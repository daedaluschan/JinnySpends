from jinny_spends_cfg import *
from jinny_spends_static import *
from spending_data import *
import logging
from logging.handlers import RotatingFileHandler

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, StringRegexHandler, jobqueue, CallbackQueryHandler)
from telegram import replykeyboardmarkup, inlinekeyboardbutton, inlinekeyboardmarkup
from telegram import replykeyboardremove

from functools import wraps


NEW_EXPENSE, CLONE_EXPENSE = range(2)

def formatting_expense(p_expense):
    logging.info("Formating expense")
    if "remark" in p_expense:
        return "On {}, we spent ${} for {}({}). Fyi: {}".format(p_expense["date"].strftime("%Y-%m-%d"),
                                                            p_expense["amt"],
                                                            p_expense["item"],
                                                            p_expense["cat"],
                                                            p_expense["remark"])
    else:
        return "On {}, we spent ${} for {}({}).".format(p_expense["date"].strftime("%Y-%m-%d"),
                                                            p_expense["amt"],
                                                            p_expense["item"],
                                                            p_expense["cat"])

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
    logging.info("Entered start()")
    markup = replykeyboardmarkup.ReplyKeyboardMarkup(keyboard=keyboard_start)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg_greeting,
                    reply_markup=markup)
    logging.info("Quiting start()")

@restricted
def show_3D_expense(bot, update):
    logging.info("Entered show_3D_expense()")
    for each_expense in load_3D_expense():
        logging.debug("expense item : {}".format(formatting_expense(each_expense)))
        bot.sendMessage(chat_id=update.message.chat_id, text=formatting_expense(each_expense))
    logging.info("Quiting show_3D_expense()")

def main():

    handler =  RotatingFileHandler(filename="logs/JinnySpends.log", maxBytes=log_file_size_lmt, backupCount=log_file_count_lmt)
    handler.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))

    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)

    logging.info("Entered main() and initialized Logger")

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(RegexHandler(regex_show_3D, show_3D_expense))

    logging.info("Going to start polling")
    updater.start_polling()


if __name__ == '__main__':
    main()

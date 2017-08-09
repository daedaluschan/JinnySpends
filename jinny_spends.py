from jinny_spends_cfg import *
from jinny_expense import *
from jinny_spends_static import *
from spending_data import *
import logging
from logging.handlers import RotatingFileHandler

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, StringRegexHandler, jobqueue, CallbackQueryHandler)
from telegram import replykeyboardmarkup, inlinekeyboardbutton, inlinekeyboardmarkup
from telegram import replykeyboardremove

from functools import wraps


NEW_EXPENSE_CAT, NEW_EXPENSE_DATE, CLONE_EXPENSE = range(3)

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

def create_clone_button(p_expense):
    inline_button = inlinekeyboardbutton.InlineKeyboardButton(text=il_button_clone,
                                                              callback_data=cb_data_clone.format(p_expense["_id"]))
    return inline_button

def create_edit_button(p_expense):
    inline_button = inlinekeyboardbutton.InlineKeyboardButton(text=il_button_edit,
                                                              callback_data=cb_data_edit.format(p_expense["_id"]))
    return inline_button

def create_delete_button(p_expense):
    inline_button = inlinekeyboardbutton.InlineKeyboardButton(text=il_button_delete,
                                                              callback_data=cb_data_delete.format(p_expense["_id"]))
    return inline_button

def show_data_set(expense_records, bot, update):
    logging.info("Entered show_data_set()")
    for each_expense in expense_records:
        logging.debug("expense item : {}".format(formatting_expense(each_expense)))
        bot.sendMessage(chat_id=update.message.chat_id, text=formatting_expense(each_expense),
                        reply_markup=inlinekeyboardmarkup.InlineKeyboardMarkup([[create_clone_button(each_expense),
                                                                                 create_edit_button(each_expense),
                                                                                 create_delete_button(each_expense)]]))
    logging.info("Quiting show_data_set()")


def fallback(bot, update):
    logging.info("Entered fallback()")
    bot.sendMessage(chat_id=update.message.chat_id, text=msg_dont_understand)
    logging.info("Quiting fallback()")
    return None

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
    show_data_set(expense_records=load_3D_expense(), bot=bot, update=update)
    logging.info("Quiting show_3D_expense()")

@restricted
def add_new_expense(bot, update):
    logging.info("Entered add_new_expense()")
    # bot.sendMessage(chat_id=update.message.chat_id)
    logging.info("Quiting add_new_expense()")
    return NEW_EXPENSE_DATE

@restricted
def process_expense_date_input(bot, update):
    logging.info("Entered process_expense_date_input()")
    # bot.sendMessage(chat_id=update.message.chat_id)
    logging.info("Quiting process_expense_date_input()")
    return NEW_EXPENSE_CAT

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

    dispatcher.add_handler(ConversationHandler(entry_points=[RegexHandler(button_new_item, add_new_expense)],
                                               states={NEW_EXPENSE_DATE: [RegexHandler(regex_date_input_pattern, process_expense_date_input)]},
                                               fallbacks=[MessageHandler(Filters.text, fallback)],
                                               run_async_timeout=conv_time_out))

    logging.info("Going to start polling")
    updater.start_polling()


if __name__ == '__main__':
    main()

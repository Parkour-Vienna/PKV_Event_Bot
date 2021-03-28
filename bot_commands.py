from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import operator
from datetime import date, timedelta
from helper import check_args
from settings import bot_settings
import gen_message

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def whotraining(update, context):
    logging.info('whotraining command called')
    if check_args(update, context, "/whotraining", ["[DAY]"], operator.gt, len(context.args)):
        message = gen_message.gen_whotraining(context.args)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def notraining(update, context):
    logging.info('notraining command called')
    user = update.message.from_user
    message = ""
    if len(context.args) == 0:
        message = gen_message.gen_notraining_0(user.first_name)
    elif check_args(update, context, "/notraining", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        message = gen_message.gen_notraining(user.first_name, context.args)
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def notomorrowtraining(update, context):
    logging.info('notomorrowtraining command called')
    if check_args(update, context, "/notomorrowtraining", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        user = update.message.from_user
        message = gen_message.gen_notomorrowtraining(user.first_name, context.args)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def help_me(update, context):
    logging.info('help command called')
    message = gen_message.gen_help()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def nexttraining(update, context):
    logging.info('nexttraining command called')
    if check_args(update, context, "/nexttraining", [], operator.ne, len(context.args)):
        message = gen_message.gen_nexttraining()
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def vote(update, context):
    logging.info('vote command called')
    if check_args(update, context, "/vote", ["[EVENT]", "[LOCATION]"], operator.lt, len(context.args)):
        user = update.message.from_user
        message = gen_message.gen_vote(user.first_name, context.args)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def votes(update, context):
    logging.info('votes command called')
    if check_args(update, context, "/votes", [], operator.gt, len(context.args)):
        message = gen_message.gen_votes()
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def spotmap(update, context):
    logging.info('spot command called')
    if check_args(update, context, "/spotmap", [], operator.ne, len(context.args)):
        message = gen_message.gen_spotmap()
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def forum(update, context):
    logging.info('forum command called')
    message = gen_message.gen_forum(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def tomorrowtraining(update, context):
    logging.info('tomorrowtraining command called')
    if check_args(update, context, "/tomorrowtraining", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        user = update.message.from_user
        reply_markup = None
        message = gen_message.gen_training(user.first_name, context.args, day=str(date.today() + timedelta(days=1)) + ".train", daystring="tomorrow ")
        if message != "Please specify time in the format HH:MM":
            keyboard = [[InlineKeyboardButton("Join", callback_data=str(user.first_name))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)


def training(update, context):
    logging.info('training command called')
    if check_args(update, context, "/training", ["[LOCATION]"], operator.lt, len(context.args)):
        user = update.message.from_user
        message = gen_message.gen_training(user.first_name, context.args)
        keyboard = [[InlineKeyboardButton("Join", callback_data=str(user.first_name))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)


def join(update, context):
    logging.info('join command called')
    query = update.callback_query
    query.answer()
    user = update.callback_query.from_user
    if user.first_name != query.data:
        message = gen_message.gen_join(user.first_name)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def main():
    logging.info('connecting bot')
    updater = Updater(bot_settings['bot_token'])
    dp = updater.dispatcher
    logging.info('initializing commands')
    dp.add_handler(CommandHandler(['training', 'train'], training))
    dp.add_handler(CommandHandler(['tomorrowtraining', 'ttraining'], tomorrowtraining))
    dp.add_handler(CommandHandler(['notomorrowtraining', 'nottraining'], notomorrowtraining))
    dp.add_handler(CommandHandler(['whotraining'], whotraining))
    dp.add_handler(CommandHandler(['notraining'], notraining))
    dp.add_handler(CommandHandler(['help', 'man', 'manual'], help_me))
    dp.add_handler(CommandHandler('vote', vote))
    dp.add_handler(CommandHandler('votes', votes))
    dp.add_handler(CommandHandler('forum', forum))
    dp.add_handler(CommandHandler('nexttraining', nexttraining))
    dp.add_handler(CommandHandler(['spotmap', 'spots'], spotmap))
    logging.info('initializing inline keyboard')
    dp.add_handler(CallbackQueryHandler(join))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

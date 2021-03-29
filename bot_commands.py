from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
import logging
import operator
from datetime import date, timedelta
import threading
from helper import check_args, write_file, open_file
from settings import bot_settings
import gen_message

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def whotraining(update, context):
    logging.info('whotraining command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    message = gen_message.gen_whotraining()
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def notraining(update, context):
    logging.info('notraining command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    user = update.message.from_user
    message = ""
    if len(context.args) == 0:
        message = gen_message.gen_notraining_0(user.first_name)
    elif check_args(update, context, "/notraining", ["TIME", "LOCATION"], operator.lt, len(context.args)):
        message = gen_message.gen_notraining(user.first_name, context.args)
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def notomorrowtraining(update, context):
    logging.info('notomorrowtraining command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    user = update.message.from_user
    message = ""
    if len(context.args) == 0:
        message = gen_message.gen_notraining_0(user.first_name,
                                               day=f"{date.today() + timedelta(days=1)}.train", daystring=" tomorrow")
    elif check_args(update, context, "/notomorrowtraining", ["TIME", "LOCATION"], operator.lt, len(context.args)):
        message = gen_message.gen_notraining(user.first_name, context.args,
                                             day=f"{date.today() + timedelta(days=1)}.train", daystring="tomorrow ")
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def help_me(update, context):
    logging.info('help command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    message = gen_message.gen_help()
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def nexttraining(update, context):
    logging.info('nexttraining command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    message = gen_message.gen_nexttraining()
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def vote(update, context):
    logging.info('vote command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    if check_args(update, context, "/vote", ["EVENT", "LOCATION"], operator.lt, len(context.args)):
        user = update.message.from_user
        message = gen_message.gen_vote(user.first_name, context.args)
        if message:
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def rm_vote(update, context):
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    logging.info('removevote command called')
    user = update.message.from_user
    message = ""
    if len(context.args) == 0:
        message = gen_message.gen_rm_vote_0(user.first_name)
    elif check_args(update, context, "/removevote", ["EVENT"], operator.lt, len(context.args)):
        message = gen_message.gen_rm_vote(user.first_name, context.args)
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def votes(update, context):
    logging.info('votes command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    message = gen_message.gen_votes()
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def spotmap(update, context):
    logging.info('spot command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    message = gen_message.gen_spotmap()
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def forum(update, context):
    logging.info('forum command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    message = gen_message.gen_forum(context.args)
    if message:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def tomorrowtraining(update, context):
    logging.info('tomorrowtraining command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    if check_args(update, context, "/tomorrowtraining", ["TIME", "LOCATION"], operator.lt, len(context.args)):
        user = update.message.from_user
        reply_markup = None
        message = gen_message.gen_training(user.first_name, context.args,
                                           day=f"{date.today() + timedelta(days=1)}.train", daystring="tomorrow ")
        if message != "Please specify time in the format HH:MM":
            keyboard = [[InlineKeyboardButton("Join", callback_data="train" + str(user.first_name))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
        if message:
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)


def training(update, context):
    logging.info('training command called')
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    if check_args(update, context, "/training", ["[LOCATION]"], operator.lt, len(context.args)):
        user = update.message.from_user
        message = gen_message.gen_training(user.first_name, context.args)
        keyboard = [[InlineKeyboardButton("Join", callback_data="train" + str(user.first_name))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if message:
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)


def join_training(update, context):
    logging.info('join_training command called')
    query = update.callback_query
    query.answer()
    user = update.callback_query.from_user
    if user.first_name != query.data[5:]:
        message = gen_message.gen_join(user.first_name)
        if message:
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def new_member(update, context):
    for user in update.message.new_chat_members:
        if user.username == 'PKV_Event_Bot':
            message = "Thanks for adding PKV_Event_Bot to your group! \n" \
                      "Do you want to add this group to the update list? " \
                      "This will notify you when new trainings are posted in https://parkourvienna.at " \
                      "as well as notify you when meetings are about to occur.\n"
            keyboard = [[InlineKeyboardButton("Yes", callback_data="yeslist"),
                         InlineKeyboardButton("No", callback_data="nolist")]]
            reply_markup = InlineKeyboardMarkup(keyboard, selective=True)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
        else:
            message = f"MWillkommen @{user.first_name} in der offiziellen Parkour Vienna Gruppe!\n\n" \
                      f"Diese Gruppe dient zur Organisation von gemeinsamen Trainings und " \
                      f"Diskussionen zum Thema Parkour.\n" \
                      f"Offtopic-Diskussionen sind hier nicht erwünscht (im Forum unter " \
                      f"https://parkourvienna.at/c/offtopic/ jedoch durchaus!)\n\n" \
                      f"Diese Gruppe unterstützt Bot-Commands, welche es dir leichter machen, " \
                      f"Trainings zu teilen oder für den Spot des Forum-Meetings abzustimmen. " \
                      f"Das /help Kommando gibt dir eine Übersicht über die anderen verfügbaren Kommandos.\n\n" \
                      f"Bitte drücke nach dem Lesen unterhalb dieser Nachricht auf den 'Gelesen und Beitreten'-Knopf.\n" \
                      f"Viel Spaß in der Community :)"
            keyboard = [[InlineKeyboardButton("Gelesen und Beitreten", callback_data="join" + str(user.first_name))]]
            reply_markup = InlineKeyboardMarkup(keyboard, selective=True)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
            if update.message.chat.type == "supergroup":
                context.bot.restrictChatMember(chat_id=update.effective_chat.id, user_id=user.id,
                                               permissions=ChatPermissions(can_send_messages=False,
                                                                           can_send_media_messages=False,
                                                                           can_send_polls=False,
                                                                           can_send_other_messages=False,
                                                                           can_add_web_page_previews=False,
                                                                           can_change_info=False,
                                                                           can_invite_users=False,
                                                                           can_pin_messages=False))


def join_chat(update, context):
    logging.info('join_chat command called')
    query = update.callback_query
    query.answer()
    user = update.callback_query.from_user
    if user.first_name == query.data[4:]:
        query.delete_message()
        if query.message.chat.type == "supergroup":
            context.bot.restrictChatMember(chat_id=update.effective_chat.id, user_id=user.id,
                                           permissions=ChatPermissions(can_send_messages=True,
                                                                       can_send_media_messages=True,
                                                                       can_send_polls=True,
                                                                       can_send_other_messages=True,
                                                                       can_add_web_page_previews=True,
                                                                       can_change_info=False,
                                                                       can_invite_users=True,
                                                                       can_pin_messages=False))


def join_list(update, context):
    logging.info('join_list command called')
    query = update.callback_query
    query.answer()
    if query.data == "yeslist":
        group_id = str(query.message.chat.id)
        group_ids = open_file("groups.list")
        if group_id not in group_ids:
            group_ids.append(group_id)
            write_file("groups.list", group_ids)
            message = "I have added this group to the update list."
        else:
            message = "This group is already on the update list."
    else:
        message = "I have not added this group to the update list."
    query.edit_message_text(text=message)


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
    dp.add_handler(CommandHandler(['removevote', 'rvote', 'rmvote', 'novote', 'deletevote', 'delvote'], rm_vote))
    dp.add_handler(CommandHandler('votes', votes))
    dp.add_handler(CommandHandler('forum', forum))
    dp.add_handler(CommandHandler('nexttraining', nexttraining))
    dp.add_handler(CommandHandler(['spotmap', 'spots'], spotmap))
    logging.info('initializing inline keyboard')
    dp.add_handler(CallbackQueryHandler(join_chat, pattern='^join'))
    dp.add_handler(CallbackQueryHandler(join_list, pattern='^yeslist$'))
    dp.add_handler(CallbackQueryHandler(join_list, pattern='^nolist$'))
    dp.add_handler(CallbackQueryHandler(join_training, pattern='^train'))
    logging.info('initializing message handlers')
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

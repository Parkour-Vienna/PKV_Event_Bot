from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import requests
import json
import logging
import operator
from datetime import datetime, date, timedelta
from helper import open_file, write_file, check_args
from settings import bot_settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

'''
def training(update, context):
    ppl_training = open_file(str(date.today()) + ".train")
    if check_args(update, context, "/training", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        user = update.message.from_user
        loc, timestamp = " ".join(context.args[1:]), context.args[0]
        try:
            datetime.strptime(str(timestamp), '%H:%M')
        except ValueError:
            message = "Please specify time in the format HH:MM"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            message = str(user.first_name) + " is training @" + str(loc).capitalize() + ", " + str(timestamp)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            ppl_training.append({'who': user.first_name, 'where': str(loc).capitalize(), 'when': str(timestamp)})
            write_file(str(date.today()) + ".train", ppl_training)
'''


def whotraining(update, context):
    if check_args(update, context, "/whotraining", ["[DAY]"], operator.gt, len(context.args)):
        if len(context.args) == 0 or str(context.args[0]).lower() == "today":
            ppl_training = open_file(str(date.today()) + ".train")
        elif str(context.args[0]).lower() == "tomorrow":
            ppl_training = open_file(str(date.today() + timedelta(days=1)) + ".train")
        else:
            message = "Invalid argument. Valid arguments are 'today', 'tomorrow'"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            return
        if not ppl_training:
            message = "Nobody is training :("
        else:
            message = "People training:\n"
            for item in ppl_training:
                message += item['who'] + " @" + item['where'] + ", " + item['when'] + "\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def notraining(update, context):
    ppl_training = open_file(str(date.today()) + ".train")
    user = update.message.from_user
    if len(context.args) == 0:
        user_trainings = [item for item in ppl_training if item['who'] == user.first_name]
        if len(user_trainings) > 1:
            message = "You have multiple Trainings planned. Please specify which one you want to delete."
        elif len(user_trainings) == 1:
            message = str(user.first_name) + " is no longer training @" + str(user_trainings[0]['where']).capitalize() \
                      + ", " + str(user_trainings[0]['when']) + " :("
            ppl_training.remove(user_trainings[0])
        else:
            message = "You have no training planned today. If you want to cancel a training tomorrow, you have to " \
                      "specify it manually. "
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        write_file(str(date.today()) + ".train", ppl_training)
    elif check_args(update, context, "/notraining", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        loc, timestamp = " ".join(context.args[1:]), context.args[0]

        try:
            datetime.strptime(str(timestamp), '%H:%M')
        except ValueError:
            message = "Please specify time in the format HH:MM"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            message = str(user.first_name) + " is no longer training @" + str(loc).capitalize() + ", " + str(
                timestamp) + " :("
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            ppl_training.remove({'who': user.first_name, 'where': str(loc).capitalize(), 'when': str(timestamp)})
            write_file(str(date.today()) + ".train", ppl_training)


def notomorrowtraining(update, context):
    if check_args(update, context, "/notomorrowtraining", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        ppl_training = open_file(str(date.today() + timedelta(days=1)) + ".train")
        loc, timestamp = " ".join(context.args[1:]), context.args[0]
        user = update.message.from_user
        try:
            datetime.strptime(str(timestamp), '%H:%M')
        except ValueError:
            message = "Please specify time in the format HH:MM"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            message = str(user.first_name) + " is no longer training @" + str(loc).capitalize() + ", " + str(
                timestamp) + " :("
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            ppl_training.remove({'who': user.first_name, 'where': str(loc).capitalize(), 'when': str(timestamp)})
            write_file(str(date.today() + timedelta(days=1)) + ".train", ppl_training)


def help_me(update, context):
    message = "Currently supported functions: \n" \
              "   /training [TIME] [LOCATION] \n" \
              "   /whotraining \n" \
              "   /nexttraining \n" \
              "   /notraining [TIME] [LOCATION] \n" \
              "   /tomorrowtraining [TIME] [LOCATION] \n" \
              "   /notomorrowtraining [TIME] [LOCATION] \n" \
              "   /vote [EVENT] [LOCATION] \n" \
              "   /votes \n" \
              "   /spots \n" \
              "   /forum [SEARCH TERMS]"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def nexttraining(update, context):
    if check_args(update, context, "/nexttraining", [], operator.ne, len(context.args)):
        message = ""
        ppl_training = open_file(str(date.today()) + ".train")
        now = datetime.now()
        now_hhmm_s = str(now.hour).rjust(2, "0") + ":" + str(now.minute).rjust(2, "0")
        now_hhmm = datetime.strptime(now_hhmm_s, '%H:%M')
        if ppl_training:
            next_time = min([datetime.strptime(item['when'], '%H:%M') for item in ppl_training])
            next_time_s = str(next_time.hour) + ":" + str(next_time.minute).rjust(2, "0")
            if next_time.time() > now_hhmm.time():
                next_training = next(item for item in ppl_training if item['when'] == str(next_time_s))
                message = "Next training is @" + next_training['where'] + " at " + next_training['when'] + " with " \
                          + next_training['who']
        if not message:
            ppl_training_tm = open_file(str(date.today() + timedelta(days=1)) + ".train")
            if ppl_training_tm:
                next_time = min([datetime.strptime(item['when'], '%H:%M') for item in ppl_training_tm])
                next_time_s = str(next_time.hour) + ":" + str(next_time.minute).rjust(2, "0")
                next_training = next(item for item in ppl_training_tm if item['when'] == str(next_time_s))
                message = "Next training is tomorrow @" + next_training['where'] + " at " + next_training[
                    'when'] + " with " + next_training['who']
        if not message:
            message = "There are no trainings left today or tomorrow :("
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def vote(update, context):
    if check_args(update, context, "/vote", ["[EVENT]", "[LOCATION]"], operator.lt, len(context.args)):
        loc, event = " ".join(context.args[1:]), str(context.args[0]).lower()
        user = update.message.from_user
        if event == "fm":
            voted = open_file("fm"".train")
        elif event == "tn":
            voted = open_file("tn"".train")
        else:
            message = "Invalid argument. Valid arguments are 'fm', 'tn'"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            return
        if user.first_name in [item['who'] for item in voted]:
            old_vote = next(item for item in voted if item["who"] == user.first_name)
            message = str(user.first_name) + " has changed their vote for " + str(event).capitalize() + " to " + str(
                loc)
            voted.remove(old_vote)
        else:
            message = str(user.first_name) + " has voted for the next " + str(event).capitalize() + " to be at " + str(
                loc)
        voted.append({'who': user.first_name, 'where': str(loc).capitalize(), 'event': str(event)})
        write_file(event + ".train", voted)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def votes(update, context):
    if check_args(update, context, "/votes", [], operator.gt, len(context.args)):
        votes_fm = open_file("fm.train")
        votes_tn = open_file("tn.train")
        if votes_fm:
            message = "Votes for next FM:\n"
            for item in votes_fm:
                message += item['who'] + ": " + item['where'] + "\n"
        else:
            message = "No votes for next FM :( \n"
        message += "\n"
        if votes_tn:
            message2 = "Votes for next TN:\n"
            for item in votes_tn:
                message2 += item['who'] + ": " + item['where'] + "\n"
        else:
            message2 = "No votes for next FM :( \n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message + message2)


def spotmap(update, context):
    if check_args(update, context, "/spotmap", [], operator.ne, len(context.args)):
        message = "https://parkourvienna.at/map"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def forum(update, context):
    message = "https://parkourvienna.at/"
    if len(context.args) == 0:
        message += "categories"
    else:
        message += "search?q=" + "%20".join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def tomorrowtraining(update, context):
    if check_args(update, context, "/tomorrowtraining", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        ppl_training = open_file(str(date.today() + timedelta(days=1)) + ".train")
        loc, timestamp = " ".join(context.args[1:]), context.args[0]
        user = update.message.from_user
        try:
            if len(str(timestamp)) in [1, 2] and 0 <= int(timestamp) <= 23:
                timestamp = timestamp.rjust(2, "0") + ":00"
            if len(str(timestamp)) == 4 and 0 <= int(timestamp[:2]) <= 23 and 0 <= int(timestamp[2:]) <= 59:
                timestamp = timestamp[:2] + ":" + timestamp[2:]
            datetime.strptime(str(timestamp), '%H:%M')
        except ValueError:
            message = "Please specify time in the format HH:MM"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            message = str(user.first_name) + " is training tomorrow @" + str(loc).capitalize() + ", " + str(timestamp)
            keyboard = [[InlineKeyboardButton("Join", callback_data=str(user.first_name))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
            this_training = {'who': user.first_name, 'where': str(loc).capitalize(), 'when': str(timestamp)}
            if this_training not in ppl_training:
                ppl_training.append(this_training)
            this_training['day'] = str(date.today() + timedelta(days=1)) + ".train"
            write_file(str(date.today() + timedelta(days=1)) + ".train", ppl_training)
            write_file("tmp.train", this_training)


def training(update, context):
    if check_args(update, context, "/training", ["[LOCATION]"], operator.lt, len(context.args)):
        ppl_training = open_file(str(date.today()) + ".train")
        loc, timestamp = " ".join(context.args[1:]), context.args[0]
        user = update.message.from_user
        try:
            if len(str(timestamp)) in [1, 2] and 0 <= int(timestamp) <= 23:
                timestamp = timestamp.rjust(2, "0") + ":00"
            if len(str(timestamp)) == 4 and 0 <= int(timestamp[:2]) <= 23 and 0 <= int(timestamp[2:]) <= 59:
                timestamp = timestamp[:2] + ":" + timestamp[2:]
            datetime.strptime(str(timestamp), '%H:%M')
        except ValueError:
            timestamp = str(datetime.now().hour).rjust(2, "0") + ":" + str(datetime.now().minute).rjust(2, "0")
            loc = " ".join(context.args)
        finally:
            message = str(user.first_name) + " is training @" + str(loc).capitalize() + ", " + str(timestamp)
            keyboard = [[InlineKeyboardButton("Join", callback_data=str(user.first_name))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
            this_training = {'who': user.first_name, 'where': str(loc).capitalize(), 'when': str(timestamp)}
            if this_training not in ppl_training:
                ppl_training.append(this_training)
            this_training['day'] = str(date.today()) + ".train"
            write_file(str(date.today()) + ".train", ppl_training)
            write_file("tmp.train", this_training)


def join(update, context):
    query = update.callback_query
    query.answer()
    user = update.callback_query.from_user
    if user.first_name != query.data:
        train = open_file("tmp.train")
        parent = train['who']
        message = str(user.first_name) + " joined " + parent + " @" + str(train['where']).capitalize() + ", " + str(
            train['when'])
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        ppl_training = open_file(train['day'])
        ppl_training.append(
            {'who': user.first_name, 'where': str(train['where']).capitalize(), 'when': str(train['when'])})
        write_file(train['day'], ppl_training)


def main():
    updater = Updater(bot_settings['bot_token'])
    dp = updater.dispatcher
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
    dp.add_handler(CallbackQueryHandler(join))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

from telegram.ext import Updater, CommandHandler
import requests
import json
import logging
import operator
from datetime import datetime, date, timedelta
from helper import open_file, write_file, check_args

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


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
    if check_args(update, context, "/notraining", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        ppl_training = open_file(str(date.today()) + ".train")
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
            write_file(str(date.today()) + ".train", ppl_training)


def tomorrowtraining(update, context):
    if check_args(update, context, "/tomorrowtraining", ["[TIME]", "[LOCATION]"], operator.lt, len(context.args)):
        ppl_training = open_file(str(date.today() + timedelta(days=1)) + ".train")
        loc, timestamp = " ".join(context.args[1:]), context.args[0]
        user = update.message.from_user
        try:
            datetime.strptime(str(timestamp), '%H:%M')
        except ValueError:
            message = "Please specify time in the format HH:MM"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            message = str(user.first_name) + " is training tomorrow @" + str(loc).capitalize() + ", " + str(timestamp)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            ppl_training.append({'who': user.first_name, 'where': str(loc).capitalize(), 'when': str(timestamp)})
            write_file(str(date.today() + timedelta(days=1)) + ".train", ppl_training)


def help(update, context):
    message = "Currently supported functions: \n" \
              "   /training [TIME] [LOCATION] \n" \
              "   /whotraining \n" \
              "   /notraining [TIME] [LOCATION] \n" \
              "   /tomorrowtraining [TIME] [LOCATION] \n" \
              "   /vote [EVENT] [LOCATION] \n" \
              "   /votes \n" \
              "   /spots \n" \
              "   /forum [SEARCH TERMS]"
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


def main():
    updater = Updater('1634462832:AAEUuVYbbfQ47VrcximEFkMlBp9HF1a9xog')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('training', training))
    dp.add_handler(CommandHandler('tomorrowtraining', tomorrowtraining))
    dp.add_handler(CommandHandler('whotraining', whotraining))
    dp.add_handler(CommandHandler('notraining', notraining))
    dp.add_handler(CommandHandler(['help', 'man', 'manual'], help))
    dp.add_handler(CommandHandler('vote', vote))
    dp.add_handler(CommandHandler('votes', votes))
    dp.add_handler(CommandHandler('forum', forum))
    dp.add_handler(CommandHandler(['spotmap', 'spots'], spotmap))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

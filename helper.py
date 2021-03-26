from telegram.ext import Updater
import json
import operator


def open_file(filename):
    try:
        with open(filename, "r") as file:
            result = json.load(file)
    except FileNotFoundError:
        result = []
    return result


def write_file(filename, dump):
    with open(filename, "w+") as file:
        json.dump(dump, file)


def check_args(update, context, name, args_needed, relation, args_given):
    if relation(args_given, len(args_needed)):
        message = "The " + name + " command requires " + str(
            len(args_needed)) + "arguments \n " + name + " " + " ".join(args_needed)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        return True

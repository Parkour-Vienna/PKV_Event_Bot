from telegram.ext import Updater
import json
import operator


def open_file(filename):
    try:
        with open("data/" + filename, "r", encoding='utf8') as file:
            result = json.load(file)
    except FileNotFoundError:
        result = []
    return result


def write_file(filename, dump):
    with open("data/" + filename, "w+", encoding='utf8') as file:
        json.dump(dump, file, ensure_ascii=False)


def check_args(update, context, name, args_needed, relation, args_given):
    if relation(args_given, len(args_needed)):
        message = "The " + name + " command requires " + str(
            len(args_needed)) + " argument(s) \n " + name + " " + " ".join(args_needed)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        return True


def rec_get(name, keys):
    head, *tail = keys
    return rec_get(name.get(head, {}), tail) if tail else name.get(head, "")


def timestring(hour, minute):
    return f"{str(hour).rjust(2, '0')}:{str(minute).rjust(2, '0')}"


def parse_time(timestamp):
    if len(str(timestamp)) in [1, 2] and 0 <= int(timestamp) <= 23:
        timestamp = f"{timestamp.rjust(2, '0')}:00"
    if len(str(timestamp)) == 4 and 0 <= int(timestamp[:2]) <= 23 and 0 <= int(timestamp[2:]) <= 59:
        timestamp = f"{timestamp[:2]}:{timestamp[2:]}"
    return timestamp

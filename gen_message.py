from datetime import datetime, date, timedelta
from helper import open_file, write_file


def gen_whotraining(args):
    message = ""
    ppl_training = []
    if len(args) == 0 or str(args[0]).lower() == "today":
        ppl_training = open_file(str(date.today()) + ".train")
    elif str(args[0]).lower() == "tomorrow":
        ppl_training = open_file(str(date.today() + timedelta(days=1)) + ".train")
    else:
        message = "Invalid argument. Valid arguments are 'today', 'tomorrow'"
    if not message:
        if not ppl_training:
            message = "Nobody is training :("
        else:
            message = "People training:\n"
            for item in ppl_training:
                message += item['who'] + " @ " + item['where'] + ", " + item['when'] + "\n"
    return message


def gen_notraining_0(username):
    ppl_training = open_file(str(date.today()) + ".train")
    user_trainings = [item for item in ppl_training if item['who'] == username]
    if len(user_trainings) > 1:
        message = "You have multiple Trainings planned. Please specify which one you want to delete."
    elif len(user_trainings) == 1:
        message = str(username) + " is no longer training @ " + str(user_trainings[0]['where']).title() \
                  + ", " + str(user_trainings[0]['when']) + " :("
        ppl_training.remove(user_trainings[0])
    else:
        message = "You have no training planned today. If you want to cancel a training tomorrow, you have to " \
                  "specify it manually. "
    write_file(str(date.today()) + ".train", ppl_training)
    return message


def gen_notraining(username, args):
    ppl_training = open_file(str(date.today()) + ".train")
    loc, timestamp = " ".join(args[1:]), args[0]
    try:
        datetime.strptime(str(timestamp), '%H:%M')
    except ValueError:
        message = "Please specify time in the format HH:MM"
    else:
        message = str(username) + " is no longer training @ " + str(loc).title() + ", " + str(
            timestamp) + " :("
        ppl_training.remove({'who': username, 'where': str(loc).title(), 'when': str(timestamp)})
        write_file(str(date.today()) + ".train", ppl_training)
    return message


def gen_notomorrowtraining(username, args):
    ppl_training = open_file(str(date.today() + timedelta(days=1)) + ".train")
    loc, timestamp = " ".join(args[1:]), args[0]
    try:
        datetime.strptime(str(timestamp), '%H:%M')
    except ValueError:
        message = "Please specify time in the format HH:MM"
    else:
        message = str(username) + " is no longer training @ " + str(loc).title() + ", " + str(
            timestamp) + " :("
        ppl_training.remove({'who': username, 'where': str(loc).title(), 'when': str(timestamp)})
        write_file(str(date.today() + timedelta(days=1)) + ".train", ppl_training)
    return message


def gen_help():
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
    return message


def gen_nexttraining():
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
            message = "Next training is tomorrow @ " + next_training['where'] + " at " + next_training[
                'when'] + " with " + next_training['who']
    if not message:
        message = "There are no trainings left today or tomorrow :("
    return message


def gen_vote(username, args):
    loc, event = " ".join(args[1:]), str(args[0]).lower()
    message = ""
    voted = []
    if event == "fm":
        voted = open_file("fm"".train")
    elif event == "tn":
        voted = open_file("tn"".train")
    else:
        message = "Invalid argument. Valid arguments are 'fm', 'tn'"
    if not message:
        if username in [item['who'] for item in voted]:
            old_vote = next(item for item in voted if item["who"] == username)
            message = str(username) + " has changed their vote for " + str(event).upper() + " to " + str(
                loc)
            voted.remove(old_vote)
        else:
            message = str(username) + " has voted for the next " + str(event).upper() + " to be @ " + str(
                loc)
        voted.append({'who': username, 'where': str(loc).title(), 'event': str(event)})
        write_file(event + ".train", voted)
    return message


def gen_votes():
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
    return message + message2


def gen_spotmap():
    message = "https://parkourvienna.at/map"
    return message


def gen_forum(args):
    message = "https://parkourvienna.at/"
    if len(args) == 0:
        message += "categories"
    else:
        message += "search?q=" + "%20".join(args)
    return message


'''
def gen_tomrrowtraining(username, args):
    ppl_training = open_file(str(date.today() + timedelta(days=1)) + ".train")
    loc, timestamp = " ".join(args[1:]), args[0]
    try:
        if len(str(timestamp)) in [1, 2] and 0 <= int(timestamp) <= 23:
            timestamp = timestamp.rjust(2, "0") + ":00"
        if len(str(timestamp)) == 4 and 0 <= int(timestamp[:2]) <= 23 and 0 <= int(timestamp[2:]) <= 59:
            timestamp = timestamp[:2] + ":" + timestamp[2:]
        datetime.strptime(str(timestamp), '%H:%M')
    except ValueError:
        message = "Please specify time in the format HH:MM"
    else:
        message = str(username) + " is training tomorrow @" + str(loc).capitalize() + ", " + str(timestamp)

        this_training = {'who': username, 'where': str(loc).capitalize(), 'when': str(timestamp)}
        if this_training not in ppl_training:
            ppl_training.append(this_training)
        this_training['day'] = str(date.today() + timedelta(days=1)) + ".train"
        write_file(str(date.today() + timedelta(days=1)) + ".train", ppl_training)
        write_file("tmp.train", this_training)
    return message
'''


def gen_training(username, args, day=str(date.today()) + ".train", daystring=""):
    ppl_training = open_file(day)
    loc, timestamp = " ".join(args[1:]), args[0]
    try:
        if len(str(timestamp)) in [1, 2] and 0 <= int(timestamp) <= 23:
            timestamp = timestamp.rjust(2, "0") + ":00"
        if len(str(timestamp)) == 4 and 0 <= int(timestamp[:2]) <= 23 and 0 <= int(timestamp[2:]) <= 59:
            timestamp = timestamp[:2] + ":" + timestamp[2:]
        datetime.strptime(str(timestamp), '%H:%M')
    except ValueError:
        if day == str(date.today()) + ".train":
            timestamp = str(datetime.now().hour).rjust(2, "0") + ":" + str(datetime.now().minute).rjust(2, "0")
            loc = " ".join(args)
        else:
            return "Please specify time in the format HH:MM"
    finally:
        message = str(username) + " is training " + daystring + "@ " + str(loc).title() + ", " + str(timestamp)
        this_training = {'who': username, 'where': str(loc).title(), 'when': str(timestamp)}
        if this_training not in ppl_training:
            ppl_training.append(this_training)
        write_file(day, ppl_training)
        this_training['day'] = str(date.today()) + ".train"
        write_file("tmp.train", this_training)
        return message


def gen_join(username):
    train = open_file("tmp.train")
    parent = train['who']
    message = str(username) + " joined " + parent + " @ " + str(train['where']).title() + ", " + str(
        train['when'])
    ppl_training = open_file(train['day'])
    ppl_training.append(
        {'who': username, 'where': str(train['where']).title(), 'when': str(train['when'])})
    write_file(train['day'], ppl_training)
    return message

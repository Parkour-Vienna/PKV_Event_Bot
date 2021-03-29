from datetime import datetime, date, timedelta
from helper import open_file, write_file, timestring, parse_time


def gen_whotraining():
    message = ""
    ppl_training = open_file(f"{date.today()}.train")
    ppl_training_tm = open_file(f"{date.today() + timedelta(days=1)}.train")
    if ppl_training or ppl_training_tm:
        for ppl, day in zip([ppl_training, ppl_training_tm], ["today", "tomorrow"]):
            if not ppl:
                message += f"\nNobody is training {day} :(\n"
            else:
                message += f"\nPeople training {day}:\n"
                for item in ppl:
                    message += f"{item['who']} @ {item['where']}, {item['when']} \n"
    else:
        message = "There are no trainings today or tomorrow :("
    return message


def gen_notraining_0(username, day=f"{date.today()}.train", daystring=" today"):
    ppl_training = open_file(day)
    user_trainings = [item for item in ppl_training if item['who'] == username]
    if len(user_trainings) > 1:
        message = f"You have multiple Trainings planned{daystring}. Please specify which one you want to delete."
    elif len(user_trainings) == 1:
        message = f"{username} is no longer training{daystring} @ {user_trainings[0]['where']}," \
                  f" {user_trainings[0]['when']}  :( "
        if user_trainings[0] in ppl_training:
            ppl_training.remove(user_trainings[0])
            write_file(day, ppl_training)
    else:
        message = "You have no training planned today. If you want to cancel a training tomorrow, you have to " \
                  "specify it manually. "
    return message


def gen_notraining(username, args, day=f"{date.today()}.train", daystring=""):
    ppl_training = open_file(day)
    loc, timestamp = " ".join(args[1:]).title(), parse_time(args[0])
    try:
        timestamp = parse_time(timestamp)
        datetime.strptime(timestamp, '%H:%M')
    except ValueError:
        message = "Please specify time in the format HH:MM."
    else:
        message = f"{username} is no longer training {daystring}@ {loc}, {timestamp} :("
        this_training = {'who': username, 'where': loc, 'when': timestamp}
        if this_training in ppl_training:
            ppl_training.remove(this_training)
            write_file(day, ppl_training)
        else:
            message = "Could not find the specified training."
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
              "   /removevote [EVENT] \n" \
              "   /votes \n" \
              "   /spots \n" \
              "   /forum [SEARCH TERMS]"
    return message


def gen_nexttraining():
    message = ""
    ppl_training = open_file(f"{date.today()}.train")
    now = datetime.now()
    now_hhmm_s = timestring(now.hour, now.minute)
    now_hhmm = datetime.strptime(now_hhmm_s, '%H:%M')
    if ppl_training:
        next_time = min([datetime.strptime(item['when'], '%H:%M') for item in ppl_training])
        next_time_s = timestring(next_time.hour, next_time.minute)
        if next_time.time() > now_hhmm.time():
            next_training = next(item for item in ppl_training if item['when'] == next_time_s)
            message = f"Next training is @ {next_training['where']} at {next_training['when']} with {next_training['who']}."
    if not message:
        ppl_training_tm = open_file(f"{date.today() + timedelta(days=1)}.train")
        if ppl_training_tm:
            next_time = min([datetime.strptime(item['when'], '%H:%M') for item in ppl_training_tm])
            next_time_s = timestring(next_time.hour, next_time.minute)
            next_training = next(item for item in ppl_training_tm if item['when'] == next_time_s)
            message = f"Next training is tomorrow @ {next_training['where']} at {next_training['when']} with {next_training['who']}."
    if not message:
        message = "There are no trainings left today or tomorrow :("
    return message


def gen_vote(username, args):
    loc, event = " ".join(args[1:]).title(), args[0].upper()
    message = ""
    voted = []
    if event == "FM":
        voted = open_file("FM"".train")
    elif event == "TN":
        voted = open_file("TN"".train")
    else:
        message = "Invalid argument. Valid arguments are 'FM', 'TN'."
    if not message:
        if username in [item['who'] for item in voted]:
            old_vote = next(item for item in voted if item["who"] == username)
            message = f"{username} has changed their vote for {event} to {loc}."
            voted.remove(old_vote)
        else:
            message = f"{username} has voted for the next {event} to be @ {loc}."
        voted.append({'who': username, 'where': loc, 'event': event})
        write_file(f"{event}.train", voted)
    return message


def gen_rm_vote(username, args):
    event = args[0].upper()
    message = ""
    if event == "FM":
        voted = open_file("FM"".train")
    elif event == "TN":
        voted = open_file("TN"".train")
    else:
        message = "Invalid argument. Valid arguments are 'FM', 'TN'."
        voted = []
    if not message:
        if username in [item['who'] for item in voted]:
            old_vote = next(item for item in voted if item["who"] == username)
            message = f"{username} has taken back their vote for {old_vote['event']} ({old_vote['where']})."
            voted.remove(old_vote)
            write_file(f"{event}.train", voted)
        else:
            message = f"You have not yet voted for {event}."
    return message


def gen_rm_vote_0(username):
    message = f"Deleting all current votes for {username}...\n"
    voted_fm = open_file("FM"".train")
    voted_tn = open_file("TN"".train")
    for votes, event in zip([voted_fm, voted_tn], ["FM", "TN"]):
        if username in [item['who'] for item in votes]:
            old_vote = next(item for item in votes if item["who"] == username)
            message += f"{username} has taken back their vote for {old_vote['event']} ({old_vote['where']}).\n"
            votes.remove(old_vote)
            write_file(f"{event}.train", votes)
    if message == f"Deleting all current votes for {username}...\n":
        message = "You have no vote to delete."
    return message


def gen_votes():
    message = ""
    votes_fm = open_file("FM.train")
    votes_tn = open_file("TN.train")
    for votes, event in zip([votes_fm, votes_tn], ["FM", "TN"]):
        if votes:
            message += f"Votes for next {event}:\n"
            for item in votes:
                message += f"{item['who']}: {item['where']}\n"
        else:
            message += f"No votes for next {event} :( \n\n"
    return message


def gen_spotmap():
    message = "https://parkourvienna.at/map"
    return message


def gen_forum(args):
    message = "https://parkourvienna.at/"
    if len(args) == 0:
        message += "categories"
    else:
        message += f"search?q={'%20'.join(args)}"
    return message


def gen_training(username, args, day=f"{date.today()}.train", daystring=""):
    ppl_training = open_file(day)
    loc, timestamp = " ".join(args[1:]).title(), parse_time(args[0])
    try:
        datetime.strptime(timestamp, '%H:%M')
    except ValueError:
        if day == f"{date.today()}.train":
            timestamp = timestring(datetime.now().hour, datetime.now().minute)
            loc = " ".join(args).title()
        else:
            return "Please specify time in the format HH:MM"
    message = f"{username} is training {daystring}@ {loc}, {timestamp}."
    this_training = {'who': username, 'where': loc, 'when': timestamp}
    if this_training not in ppl_training:
        ppl_training.append(this_training)
    write_file(day, ppl_training)
    this_training['day'] = f"{date.today()}.train"
    write_file("tmp.train", this_training)
    return message


def gen_join(username):
    train = open_file("tmp.train")
    parent = train['who']
    day = ""
    if train['day'] != date.today():
        day = "tomorrow "
    message = f"{username} joined {parent} {day}@ {train['where']}, {train['when']}."
    ppl_training = open_file(train['day'])
    ppl_training.append(
        {'who': username, 'where': train['where'], 'when': train['when']})
    write_file(train['day'], ppl_training)
    return message

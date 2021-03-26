#!usr/bin/python3.9

from forum import Forum
import logging
import datetime
from helper import open_file

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('initializing forum connection')
    f = Forum('http://beta.parkourvienna.at', 'Spotbot',
              '2d6a1397fafdb361d9f4e3236d14e8cb3c1418de93883cd53cf7ad34ffe932e1')
    logging.info('testing connectivity')
    f.check_connection()

    todayday = datetime.datetime.today().weekday()
    message = ""

    logging.info('checking day')
    if todayday == 2:
        votes_tn = open_file("tn.train")
        if votes_tn:
            message = "Votes for this TN:\n"
            for item in votes_tn:
                message += item['who'] + ": " + item['where'] + "\n"
        else:
            message = "No votes from Chats for this FM :( \n"

    if todayday == 6:
        votes_fm = open_file("fm.train")
        if votes_fm:
            message = "Votes for this FM:\n"
            for item in votes_fm:
                message += item['who'] + ": " + item['where'] + "\n"
        else:
            message = "No votes from Chats for this FM :( \n"

    if todayday == 2 or todayday == 6:
        logging.info('making post')
        f.create_post(839, message)
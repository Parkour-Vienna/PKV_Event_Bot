#!usr/bin/python3.9

import requests
import logging
import datetime
from helper import open_file
from settings import bot_settings

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    todayday = datetime.datetime.today().weekday()
    message = ""

    logging.info('checking day')
    if todayday == 2:
        votes_tn = open_file("tn.train")
        message = "*Voting for Tuesdayness will close in 2 hours! \nMake sure to get your vote in with /vote TN \[" \
                  "SPOT]! \nThe following people have voted already: " + " ".join([item['who'] for item in votes_tn])

    if todayday == 6:
        votes_fm = open_file("fm.train")
        message = "*Voting for Forum Meeting will close in 2 hours!* \nMake sure to get your vote in with /vote FM \[" \
                  "SPOT]! \n\nThe following people have voted already:\n   " + " ".join([item['who'] for item in votes_fm])

    if todayday == 2 or todayday == 6:
        for group in bot_settings['bot_chatID']:
            send = 'https://api.telegram.org/bot' + bot_settings['bot_token'] + '/sendMessage?chat_id=' + group + \
                   '&parse_mode=markdown' + '&text=' + message
            requests.get(send)

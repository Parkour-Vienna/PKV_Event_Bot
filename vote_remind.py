#!usr/bin/python3.9

import requests
import logging
import datetime

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot_token, bot_chatID = '1634462832:AAEUuVYbbfQ47VrcximEFkMlBp9HF1a9xog', '-550704351'
    todayday = datetime.datetime.today().weekday()
    message = ""

    logging.info('checking day')
    if todayday == 2:
        message = "*Voting for Tuesdayness will close in 2 hours! \nMake sure to get your vote in with /vote TN \[" \
                  "SPOT]! "

    if todayday == 6:
        message = "*Voting for Forum Meeting will close in 2 hours!* \nMake sure to get your vote in with /vote FM \[" \
                  "SPOT]! "

    if todayday == 2 or todayday == 6:
        send = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + \
               '&parse_mode=markdown' + '&text=' + message
        requests.get(send)

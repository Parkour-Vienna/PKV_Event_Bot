#!usr/bin/python3.9

from forum import Forum
import logging
import datetime
from helper import open_file
from settings import api_settings

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('initializing forum connection')
    f = Forum(api_settings['forum_url'], api_settings['api_name'], api_settings['api_key'])
    logging.info('testing connectivity')
    f.check_connection()

    todayday = datetime.datetime.today().weekday()
    message = ""
    t_id = 0

    logging.info('checking day')
    topics = [dic for dic in f.get_latest_topics(5)['topic_list']['topics'] if dic['pinned'] is False][:10]
    if todayday == 2:
        votes_tn = open_file("tn.train")
        if votes_tn:
            message = "Votes for this TN:\n"
            for item in votes_tn:
                message += item['who'] + ": " + item['where'] + "\n"
        else:
            message = "No votes from Chats for this FM :( \n"
        t_id = next(item['id'] for item in topics if "Tuesdayness" in item['title'])

    if todayday == 5:
        votes_fm = open_file("fm.train")
        if votes_fm:
            message = "Votes for this FM:\n"
            for item in votes_fm:
                message += item['who'] + ": " + item['where'] + "\n"
        else:
            message = "No votes from Chats for this FM :( \n"
        t_id = next(item['id'] for item in topics if "Forum Meeting" in item['title'])

    if t_id and (todayday == 2 or todayday == 5):
        logging.info('making post')
        f.create_post(t_id, message)

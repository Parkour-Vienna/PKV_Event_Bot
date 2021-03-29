#!usr/bin/python3.9

from forum import Forum
import requests
import logging
import dateutil.parser as DP
from settings import api_settings, bot_settings, route_settings

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('initializing forum connection')
    f = Forum(api_settings['forum_url'], api_settings['api_name'], api_settings['api_key'])
    logging.info('testing connectivity')
    f.check_connection()
    
    logging.info('getting new topics')
    dif = f.compare_topics(5, ['id'], ['slug'], ['excerpt'], ['tags'], ['created_at'], ['title'], ['event', 'start'])
    if dif:
        logging.info(str(len(dif)) + 'new topics found, iterating through')
        for item in dif:
            tag_txt = start_txt = ""

            if len(item['excerpt']) == 100:
                item['excerpt'] = item['excerpt'][:97] + "..."
            if item['tags']:
                tag_txt = "(Tags: " + str(item['tags']) + ")"
            if item['event, start']:
                start_txt = "*Wann:* " + str(DP.parse(item['event, start']))[:20] + "\n"

            for group in bot_settings['bot_chatID']:
                body = "*" + item['title'] + "* " + tag_txt + "\n\n" + item['excerpt'] + "\n\n" + start_txt + \
                       "http://beta.parkourvienna.at/t/" + item['slug'] + "/" + str(item['id'])
                send = 'https://api.telegram.org/bot' + bot_settings['bot_token'] + '/sendMessage?chat_id=' + group + \
                       '&parse_mode=markdown' + '&text=' + body

                if route_settings['text_dest'] == "whatsapp":
                    logging.info('making transfer file for whatsapp')
                    with open('transfer.tmp', "w") as file:
                        file.write(str(send))
                elif route_settings['text_dest'] == "telegram":
                    logging.info('sending message to telegram')
                    requests.get(send)
    else:
        logging.info('no new topics')


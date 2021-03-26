#!usr/bin/python3.9

from forum import Forum
import requests
import logging
import dateutil.parser as DP

dest = "whatsapp"
bot_token, bot_chatID = '1634462832:AAEUuVYbbfQ47VrcximEFkMlBp9HF1a9xog', '-550704351'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('initializing forum connection')
    f = Forum('http://beta.parkourvienna.at', 'Spotbot', '2d6a1397fafdb361d9f4e3236d14e8cb3c1418de93883cd53cf7ad34ffe932e1')
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
                
            body = "*" + item['title'] + "* " + tag_txt + "\n\n" + item['excerpt'] + "\n\n" + start_txt + "http://beta.parkourvienna.at/t/" + item['slug'] + "/" + str(item['id'])
            send = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=markdown' + '&text=' + body
            
            if dest == "whatsapp":
                logging.info('making transfer file for whatsapp')
                with open('transfer.tmp', "w") as file:
                    file.write(str(send))
            elif dest == "telegram":
                logging.info('sending message to telegram')
                requests.get(send)
    else:
        logging.info('no new topics')


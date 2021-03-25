from forum import Forum
import requests
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('initializing forum connection')
    f = Forum('http://beta.parkourvienna.at', 'Spotbot', '2d6a1397fafdb361d9f4e3236d14e8cb3c1418de93883cd53cf7ad34ffe932e1')
    logging.info('testing connectivity')

    dif = f.compare_topics(5)
    print(dif)
    if dif:
        for item in dif:
            tag_txt = ""
            bot_token = '1634462832:AAEUuVYbbfQ47VrcximEFkMlBp9HF1a9xog'
            bot_chatID = '-1001165535219'
            if len(item['excerpt']) == 100:
                item['excerpt'] = item['excerpt'][:97] + "..."
            if item['tags']:
                tag_txt = "(Tags: " + str(item['tags']) + ")"
            body = "*" + item['title'] + "* " + tag_txt + ":\n\n" + item['excerpt'] + "\n\n" + "http://beta.parkourvienna.at/t/" + item['slug'] + "/" + str(item['id'])
            send = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=markdown' + '&text=' + body
            requests.get(send)
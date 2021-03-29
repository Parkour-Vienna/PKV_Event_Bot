from helper import open_file

api_settings = {
    'forum_url': 'http://beta.parkourvienna.at',
    'api_name': 'Spotbot',
    'api_key': '2d6a1397fafdb361d9f4e3236d14e8cb3c1418de93883cd53cf7ad34ffe932e1'
}

bot_settings = {
    'bot_token': '1634462832:AAEUuVYbbfQ47VrcximEFkMlBp9HF1a9xog',
    'bot_chatID': open_file("groups.list")
}

route_settings = {
    'text_dest': "telegram"
}
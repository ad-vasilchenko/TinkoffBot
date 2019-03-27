import requests  
import datetime
from time import sleep

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

token = '867587456:AAHLtFqnmhSyhhaWerqE2D-sZ0_PQetrOSA'
yt_token = 'trnsl.1.1.20190327T140319Z.26c39ab07e9607fe.cab07c62a79e982113bffce226374ad14ef30089'
greet_bot = BotHandler(token)  

def main():  
    new_offset = None
    while True:
        greet_bot.get_updates(new_offset)

        data = greet_bot.get_last_update()
        update_id = data['update_id']
        chat_id  = data['message']['chat']['id']
        
        if update_id == data['update_id']:
            try:
                payload = {'key':yt_token,'text': data['message']['text'],'lang':'ru-en'}
                translate = requests.post("https://translate.yandex.net/api/v1.5/tr.json/translate",data=payload).json()['text']
                greet_bot.send_message(chat_id, translate)
            except:
                greet_bot.send_message(chat_id, "Ошибка")
                
        sleep(1)   

        new_offset = update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
"""
setup:
    pip install requests
    pip install requests[socks]
super helpful:
    - http://packetforger.wordpress.com/2013/08/27/pythons-requests-module-with-socks-support-requesocks/
    - http://docs.python-requests.org/en/master/user/advanced/#proxies

    - На ПК установить и покдлючить OpenVPN
    - https://ukproxy.vpnbook.com/browse.php?u=UMtRLTYMavtadW8fUF3X4I7MmOrXfc2aDmYDp1OO&b=0&f=norefer#getting-updates
    - https://core.telegram.org/bots/api
"""

import requests
import misc
import json
from yobit import get_btc
from time import sleep

global last_update_id
last_update_id = 0

proxies = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}

token = misc.token

URL = 'https://api.telegram.org/bot' + token + '/'


def get_updates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    return r.json()

def get_message():
    # Отвечать только на новые сообщения

    # Получаем update_id каждого обновления
    # записываем в переменную, а затем сранивать с update_id
    # последнего элемента в списке result

    data = get_updates()

    last_object = data['result'][-1]

    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']

        message_text = last_object['message']['text']
        print(message_text)
        message = {'chat_id': chat_id,
                        'text': message_text}
        return message
    return None


def send_message(chat_id, text='Wait a second, please...'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    #print(url)
    requests.get(url)

def main():
    #d = get_updates()
    #with open('updates.json', 'w') as file:
     #   json.dump(d, file, indent=2, ensure_ascii=False)
    #print(get_message())
    #send_message(238121714, 'ку ку')

    # вызов бесконечного цикла
    while True:
        answer = get_message()

        if answer != None:
            chat_id = answer['chat_id']
            text = answer['text']

            if text == '/btc':
                send_message(chat_id, get_btc())

            else:
                continue

        sleep(2) #сон

if __name__ == '__main__':
    main()

# https://api.telegram.org/bot559711066:AAF01nkpNlNr9VEmayeTgKnfM3LuPG0dfmg/sendMessage?chat_id=238121714&text=hi
# https://api.telegram.org/bot559711066:AAF01nkpNlNr9VEmayeTgKnfM3LuPG0dfmg/getUpdates

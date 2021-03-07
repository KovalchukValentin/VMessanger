import requests
from db_client import DB

url = "http://127.0.0.1:5000/"
class Client:
    def __init__(self):
        user_info = db.get_user()
        self.user_id = user_info
        self.chat_id = 0
        self.name = "Unnamed"
        self.send = url + 'send'
        self.messages = url + 'messages'
        self.singup = url + 'sing_up'
        self.last_time = "0-0-0 0:0:0:0"

    def send_message(self, text):
        requests.post(self.send, json={'name': self.name, 'text': text})

    def get_messages(self):
        response = requests.get(self.messages, params={'last_time': self.last_time, 'user_id': self.user_id, 'chat_id': self.chat_id}).json()

        if not isinstance(response, dict) or set(response) != {'messages'}:
            return -1
        response = response['messages']

        for message in response:
            print(f'{message["name"]}: {message["text"]}\n{message["time"]}\n')
            self.last_time = message["time"]

    def sing_up(self, user_id):
        requests.post(self.singup, json={'user_id': user_id})


if __name__ == '__main__':
    db = DB()
    app = Client()
    app.get_messages()
    while True:
        app.send_message(str(input()))
        app.get_messages()


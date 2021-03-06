import requests
from time import time
url = "http://127.0.0.1:5000/"
class Client:
    def __init__(self, name):
        self.name = name
        self.send = url + 'send'
        self.messages = url + 'messages'
        self.after = 0

    def send_message(self, text):
        requests.post(self.send, json={'name': self.name, 'text': text})

    def get_messages(self):
        response = requests.get(self.messages, params={'after': self.after}).json()

        if not isinstance(response, dict) or set(response) != {'messages'}:
            return -1
        response = response['messages']
        self.after = time()
        for message in response:
            print(f'{message["name"]}: {message["text"]}\n{message["time"]}\n')

    def update(self):
        print()

app = Client("Lolik")
app.get_messages()
while True:
    app.send_message(str(input()))
    app.get_messages()


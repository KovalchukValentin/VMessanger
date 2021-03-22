import requests
from db_client import DB

URL = "http://127.0.0.1:5000/"

class Client:
    def __init__(self):
        self.URLS = {'send': URL + 'send',
                     'messages': URL + 'messages',
                     'sing_up': URL + 'sing_up',
                     'sing_in': URL + 'sing_in',
                     'create_chat': URL + 'create_chat',
                     'add_contact': URL + 'add_contact'}
        self.current_chat_id = None
        user_info = db.get_user()

        if user_info is None:
            self.last_time = "0-0-0 0:0:0:0"
            self.user_name = input("Введите свой никнейм: ")
            self.user_id = self.sing_up(self.user_name)
            db.save_user_if_not_exists(user_id=self.user_id, user_name=self.user_name, last_time=self.last_time)
            print("Success sing in")
        else:
            self.last_time = user_info['last_time']
            self.user_id = user_info['user_id']
            self.user_name = user_info['user_name']
        print("Name: ", self.user_name,
                  "\nID: ", self.user_id,
                  "\nLast time: ", self.last_time )


    def send_message(self, text):
        requests.post(self.URLS['send'], json={'chat_id': self.current_chat_id, 'user_id': self.user_id, 'text': text})

    def get_messages(self):
        response = requests.get(self.URLS['messages'], params={'last_time': self.last_time, 'user_id': self.user_id}).json()

        if not isinstance(response, dict) or set(response) != {'messages'}:
            return -1
        response = response['messages']

        for message in response:
            print(f'{message["name"]}: {message["text"]}\n{message["time"]}\n')
            self.last_time = message["time"]

    def sing_up(self, name):
        user_id = requests.post(self.URLS['sing_up'], json={'name': name}).json()['user_id']
        if user_id is None:
            user_id = self.sing_in(name)
        return user_id

    def sing_in(self, name):
        user_id = requests.get(self.URLS['sing_in'], params={'name': name}).json()['user_id']
        return user_id

    def create_chat(self, user2_id):
        response = requests.get(url=self.URLS['create_chat'], params={'user1_id': self.user_id, 'user2_id': user2_id})

    def add_contact(self, contact_name):
        response = requests.post(self.URLS['add_contact'], json={'user_id': self.user_id, 'contact_name': contact_name})
    def log_out(self):
        db.remove_user()

if __name__ == '__main__':
    db = DB()
    app = Client()
    app.add_contact('lol')
    app.add_contact('nice')
    app.add_contact('hell')
    if input('Log out?') == "y":
        app.log_out()

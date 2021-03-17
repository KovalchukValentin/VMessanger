import requests
from db_client import DB

url = "http://127.0.0.1:5000/"
class Client:
    def __init__(self):
        self.urls = {'send': url + 'send',
                     'messages': url + 'messages',
                     'sing_up': url + 'sing_up',
                     'sing_in': url + 'sing_in'}
        self.current_chat_id = None
        user_info = db.get_user()

        if user_info == None:
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
        requests.post(self.urls['send'], json={'chat_id': self.current_chat_id, 'user_id': self.user_id, 'text': text})

    def get_messages(self):
        response = requests.get(self.urls['messages'], params={'last_time': self.last_time, 'user_id': self.user_id, 'chat_id': self.current_chat_id}).json()

        if not isinstance(response, dict) or set(response) != {'messages'}:
            return -1
        response = response['messages']

        for message in response:
            print(f'{message["name"]}: {message["text"]}\n{message["time"]}\n')
            self.last_time = message["time"]

    def sing_up(self, name):
        user_id = requests.post(self.urls['sing_up'], json={'name': name}).json()['user_id']
        if user_id == None:
            user_id = self.sing_in(name)
        return user_id

    def sing_in(self, name):
        user_id = requests.get(self.urls['sing_in'], params={'name': name}).json()['user_id']
        return user_id

    def log_out(self):
        db.remove_user()

if __name__ == '__main__':
    db = DB()
    app = Client()
    if input('Log out?') == "y":
        app.log_out()
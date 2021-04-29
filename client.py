import requests
import os

URL = "http://127.0.0.1:5000/"


class Client:
    def __init__(self):
        self.URLS = {'send': URL + 'send',
                     'messages': URL + 'messages',
                     'sing_up': URL + 'sing_up',
                     'sing_in': URL + 'sing_in',
                     'create_chat': URL + 'create_chat',
                     'add_contact': URL + 'add_contact',
                     'contacts': URL + 'contacts',
                     'chat_id': URL + "chat_id"}
        self.current_chat = None

    def set_user(self, last_time=None, user_name=None, user_id=None, password=None):
        if last_time is None:
            last_time = "0-0-0 0:0:0:0"
        if user_name is None and user_id is None:
            self.user_name = user_name
            self.user_id = user_id
            self.last_time = last_time
        elif not user_id is None and not user_name is None:
            self.user_id = user_id
            self.user_name = user_name
            self.last_time = last_time
        self.password = password
        try:
            self.contacts = self.get_contacts()
        except:
            pass
        # elif not user_name is None:
        #     self.user_name = user_name
        #     self.user_id = self.sing_up(self.user_name)
        #     self.last_time = last_time

    def get_user(self):
        return {'id': self.user_id, 'name': self.user_name, 'last_time': self.last_time, 'password': self.password}

    def send_message(self, text):
        requests.post(self.URLS['send'], json={'chat_id': self.current_chat['chat_id'], 'user_id': self.user_id, 'text': text})

    def get_messages(self):
        response = requests.get(self.URLS['messages'], params={'last_time': self.last_time, 'user_id': self.user_id}).json()

        if not isinstance(response, dict) or set(response) != {'messages', 'time'}:
            return -1
        self.last_time = response['time']
        return response['messages']

    def sing_up(self, name: str, password: str):
        if name is None or password is None:
            return None

        if not isinstance(name, str) or not isinstance(password, str):
            return None

        response = requests.post(self.URLS['sing_up'], json={'name': name, 'password': password}).json()
        if response is None:
            return None
        if set(response) == {'password'}:
            return {'attention': response['password']}
        if set(response) == {'user_id'}:
            return {'user_id': response['user_id']}

    def sing_in(self, name, password):
        user_id = requests.get(self.URLS['sing_in'], params={'name': name, 'password': password}).json()['user_id']
        return user_id

    def create_chat(self, user2_id):
        response = requests.get(url=self.URLS['create_chat'], params={'user1_id': self.user_id, 'user2_id': user2_id})

    def add_contact(self, contact_name=None, contact_id=None):
        response = requests.post(self.URLS['add_contact'], json={'user_id': self.user_id,
                                                                 'contact_name': contact_name,
                                                                 'contact_id': contact_id}).json()
        if set(response) == {'result', 'contact_id'}:

            if response['result'] == 'ok':
                self.contacts.append((response['contact_id'], response['contact_name']))

        return response

    def log_out(self):
        self.current_chat = None
        self.set_user()

    def get_contacts(self):
        response = requests.get(url=self.URLS['contacts'], params={'user_id': self.user_id}).json()
        return response['contacts']

    def check_name(self, name):
        if len(name) > 14:
            return 'longname'
        if name == '':
            return 'empty'

        good_letters = 'qwertyuiopasdfghjklzxcvbnm1234567890_'

        for letter in name:
            if not letter in good_letters:
                return 'badname'
        return None

    def check_password(self, password):
        attention = None
        if len(password) < 8:
            attention = 'smallpassword'
        elif password.isdigit():
            attention = 'needletter'
        elif password == password.lower():
            attention = 'needupper'
        elif password == password.upper():
            attention = 'needlower'
        return attention

    def get_chat_id(self, contact_id):
        if not isinstance(contact_id, int):
            return
        response = requests.get(url=self.URLS['chat_id'], params={'user_id': self.user_id, 'contact_id': contact_id}).json()
        return response['chat_id']

    def isincontacts(self, contact_id):
        if contact_id == self.user_id:
            return True
        if self.contacts is None:
            return False
        print(self.contacts)
        contacts = [contact_id[0] for contact_id in self.contacts]
        if contacts is None:
            return False
        for contact in contacts:
            if int(contact) == int(contact_id):
                return True
        return False

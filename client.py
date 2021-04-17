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
        self.current_chat_id = None

    def set_user(self, last_time=None, user_name=None, user_id=None):
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
        elif not user_name is None:
            self.user_name = user_name
            self.user_id = self.sing_up(self.user_name)
            self.last_time = last_time

    def get_user(self):
        return {'id': self.user_id, 'name': self.user_name, 'last_time': self.last_time}

    def send_message(self, text):
        requests.post(self.URLS['send'], json={'chat_id': self.current_chat_id, 'user_id': self.user_id, 'text': text})

    def get_messages(self):
        response = requests.get(self.URLS['messages'], params={'last_time': self.last_time, 'user_id': self.user_id}).json()

        if not isinstance(response, dict) or set(response) != {'messages'}:
            return -1

        return response['messages']

    def sing_up(self, name):
        if name is None:
            return None

        user_id = requests.post(self.URLS['sing_up'], json={'name': name}).json()['user_id']
        if user_id is None:
            return None
        return user_id

    def sing_in(self, name):
        user_id = requests.get(self.URLS['sing_in'], params={'name': name}).json()['user_id']
        return user_id

    def create_chat(self, user2_id):
        response = requests.get(url=self.URLS['create_chat'], params={'user1_id': self.user_id, 'user2_id': user2_id})

    def add_contact(self, contact_name):
        response = requests.post(self.URLS['add_contact'], json={'user_id': self.user_id, 'contact_name': contact_name}).json()
        return response['request']

    # def log_out(self):
    #     db.remove_user()

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
        return 0

    def get_chat_id(self, contact_id):
        if not isinstance(contact_id, int):
            return
        response = requests.get(url=self.URLS['chat_id'], params={'user_id': self.user_id, 'contact_id': contact_id}).json()
        return response['chat_id']


# class ConsoleApp:
#     def __init__(self):
#         self.current_window = 'menu'
#         self.client = Client()
#         self.end = False
#         self.pointer_menu = 0
#         self.commands_main_menu = ['profile', 'contacts', 'add_contact', 'logout']
#
#     def run(self):
#         while not self.end:
#             if self.current_window == 'menu':
#                 self.print_menu()
#                 self.processing_input_command()
#             elif self.current_window == 'profile':
#                 self.print_profile()
#                 self.processing_input_command()
#             elif self.current_window == 'contacts':
#                 self.print_contacts(self.client.get_contacts())
#                 self.processing_input_command()
#             elif self.current_window == 'add_contact':
#                 self.print_add_contact()
#                 # self.processing_input_command()
#             self.clear_scr()
#
#     def print_profile(self):
#         pass
#
#     def processing_input_command(self):
#         input_command = input()
#         if input_command.lower() == 'w':
#             self.pointer_menu -= 1
#             if self.pointer_menu == -1:
#                 self.pointer_menu = len(self.commands_main_menu) - 1
#         elif input_command.lower() == 's':
#             self.pointer_menu += 1
#             if self.pointer_menu == len(self.commands_main_menu):
#                 self.pointer_menu = 0
#         elif input_command.lower() == 'quit':
#             self.end = True
#         elif input_command.lower() == 'b' and self.current_window != 'menu':
#             self.current_window = 'menu'
#             self.pointer_menu = 0
#         elif input_command == '':
#             self.do_command(self.commands_main_menu[self.pointer_menu])
#
#     def do_command(self, command: str):
#         if command == 'profile':
#             self.current_window = command
#         elif command == 'contacts':
#             self.pointer_menu = 0
#             self.current_window = command
#         elif command == 'add_contact':
#             self.current_window = command
#         elif command == 'logout':
#             self.client.log_out()
#             exit()
#
#     def clear_scr(self):
#         os.system('cls')
#
#     def print_add_contact(self):
#         contact_name = input("Input name of your contact:")
#         result = self.client.add_contact(contact_name=contact_name)
#         if result == 'is_your_name':
#             print('Is your name')
#             if input('Try more? (Y/N)').lower() != 'y':
#                 self.current_window = "menu"
#         elif result == 'contact_is_not_exist':
#             print('Contact is not exist')
#             if input('Try more? (Y/N)').lower() != 'y':
#                 self.current_window = "menu"
#         elif result == 'contact_is_in_contacts':
#             print('Contact is in contacts')
#             if input('Add more? (Y/N)').lower() != 'y':
#                 self.current_window = "menu"
#         elif result == 'ok':
#             print('Contact has been added')
#             if input('Add more? (Y/N)').lower() != 'y':
#                 self.current_window = "menu"
#
#     def print_contacts(self, contacts):
#         if contacts is None:
#             print("Contacts list is empty")
#             return
#         for num, contact in enumerate(contacts):
#             if num == self.pointer_menu:
#                 print('>', str(num + 1) + '.' + contact)
#             else:
#                 print(' ', str(num + 1) + '.' + contact)
#
#     def print_menu(self):
#         print("Name: ", self.client.user_name,
#               "|ID: ", self.client.user_id,
#               "|Last time: ", self.client.last_time)
#         for num, command in enumerate(self.commands_main_menu):
#             if num == self.pointer_menu:
#                 print('>', str(num + 1) + '.' + command)
#             else:
#                 print(' ', str(num + 1) + '.' + command)


# if __name__ == '__main__':
#     app = ConsoleApp()
#     app.run()

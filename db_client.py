import sqlite3

# User
# user_id
# last_time


class DB:
    def __init__(self):
        self.dateformat = '%d-%m-%Y %H:%M:%S:%f'
        self.conn = sqlite3.connect('VMessangerC.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS User (id integer,
                                                           name text,
                                                           password text,
                                                           last_time text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS Messages(id integer, 
                                                                chat_id integer,
                                                                user_id integer,
                                                                txt text,
                                                                time text)''')

    def save_user_if_not_exists(self, user: dict):
        if set(user) != {'id', 'name', 'last_time', 'password'}:
            # print('non')
            return 0
        # print(user['id'], user['name'], user['last_time'])
        user_id = self.get_user()['user_id']
        if user_id is None:
            self.c.execute('''INSERT INTO User (id, name, last_time, password) VALUES (?, ?, ?, ?)''',
                           (user['id'], user['name'], user['last_time'], user['password']))
        elif user_id == user['id']:
            self.c.execute('''UPDATE User SET last_time=?, name=?, password=? WHERE id=?''',
                           (user['last_time'], user['name'], user['password'], user['id']))
        else:
            return 0
        self.conn.commit()

    def get_user(self):
        user = [i for i in self.c.execute('''SELECT id, name, last_time FROM User''')]
        if user == []:
            return {'user_id': None, 'user_name': None, 'last_time': None}
        return {'user_id': user[0][0], 'user_name': user[0][1], 'last_time': user[0][2]}

    def remove_user(self):
        self.c.execute('''DELETE From User''')
        self.c.execute('''DELETE From Messages''')
        self.conn.commit()

    def save_messages(self, messages: list) -> dict:
        if not isinstance(messages, list):
            return {'ok': False}
        # print(messages)
        for message in messages:
            if set(message) != {'id', 'chat_id', 'user_id', 'text', 'time'}:
                return {'ok': False}
            message_id = message['id']
            chat_id = message['chat_id']
            user_id = message['user_id']
            text = message['text']
            time = message['time']
            self.c.execute('''INSERT INTO Messages (id, chat_id, user_id, txt, time) VALUES (?, ?, ?, ?, ?)''',
                            (message_id, chat_id, user_id, text, time))
        return {'ok': True}

    def get_messages_from_chat(self, chat_id):
        messages = [i for i in self.c.execute(f'''SELECT id, chat_id, user_id, txt, time FROM Messages WHERE chat_id="{str(chat_id)}"''')]
        result = []
        if messages != []:
            for message in messages:
                result.append({'id': message[0],
                                 'chat_id': message[1],
                                 'user_id': message[2],
                                 'text': message[3],
                                 'time': message[4]})
        if result == []:
            result = None
        return result
import sqlite3
from datetime import datetime

# Users
# user_id
# user_avatar (wait)
# user_name
# user_description (wait)

# Chats
# chat_id
# chat_img (wait)
# users_id (list user_id in chat)

# Messages
# message_id
# user_id
# chat_id
# txt
# time
# edited bool (wait)

# Contacts
# contact_id
# user_id
# users_id (list user_id in contacts )


class DB:
    def __init__(self):
        self.dateformat = '%d-%m-%Y %H:%M:%S:%f'

        conn = self.connect_bd()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Users (id integer primary key,
                                                            name text, 
                                                            password text)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Messages (id integer primary key,
                                                               chat_id integer,
                                                               user_id integer,
                                                               txt text, 
                                                               time text)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Chats (id integer primary key,
                                                            user1_id integer,
                                                            user2_id integer)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Contacts (id integer primary key,
                                                               user_id integer,
                                                               users_id text)''')
        conn.commit()
        conn.close()

    def connect_bd(self):
        return sqlite3.connect('VMessangerS.db')

    def check_used_name(self, name):
        conn = self.connect_bd()
        cur = conn.cursor()
        user_id = [i for i in cur.execute(f'''SELECT id FROM Users WHERE name="{name}"''')]
        result = False
        if user_id != []:
            result = True
        conn.close()
        return result

    def add_user(self, name, password):
        if name == 'name':
            return False
        conn = self.connect_bd()
        cur = conn.cursor()
        is_used_name = self.check_used_name(name=name)
        if not is_used_name:
            cur.execute(f'''INSERT INTO Users (name, password) VALUES ("{name}", "{password}")''')
            conn.commit()
            result = True
        else:
            result = False
        conn.close()
        return result

    def add_message(self, chat_id, user_id, text):
        conn = self.connect_bd()
        cur = conn.cursor()
        cur.execute('''INSERT INTO Messages (chat_id, user_id, txt, time) VALUES (?, ?, ?, ?)''',
                    (chat_id, user_id, text, self.get_now_time()))
        conn.commit()
        conn.close()

    def add_chat_if_not_exist(self, user1_id, user2_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        chat_id = self.get_chat_id(user1_id, user2_id)
        if chat_id is None:
            cur.execute('''INSERT INTO Chats (user1_id, user2_id) VALUES (?, ?)''', (user1_id, user2_id))
            conn.commit()
            result = self.get_chat_id(user1_id, user2_id)
        else:
            result = chat_id
        conn.close()
        return result

    def add_contact(self, user_id: int, contact_name=None, contact_id=None):
        if not contact_name is None:
            need_add_contact_id = self.get_contact_id(contact_name)
        elif not contact_id is None:
            need_add_contact_id = contact_id
            contact_name = self.get_user(contact_id)
        else:
            return {'result': 'wrong_input'}

        if contact_name == 'name':
            return {'result': 'contact_is_not_exist'}

        contacts_id = self.get_contacts(user_id=user_id)

        if need_add_contact_id is None:
            return {'result': 'contact_is_not_exist'}

        if self.isincontacts(user_id, need_add_contact_id):
            return {'result': 'contact_is_in_contacts'}

        if need_add_contact_id == user_id:
            return {'result': 'is_your_name'}

        conn = self.connect_bd()
        cur = conn.cursor()

        if contacts_id is None:
            cur.execute('''INSERT INTO Contacts (user_id, users_id) VALUES (?, ?)''',
                        (user_id, str(need_add_contact_id)))
        else:
            contacts_id.append(str(need_add_contact_id))
            contacts_id = ' '.join(contacts_id)
            cur.execute('''UPDATE Contacts SET users_id=? WHERE user_id=?''',
                        (contacts_id, user_id))
        conn.commit()
        conn.close()
        return {'result': 'ok', 'contact_id': need_add_contact_id, 'contact_name': contact_name}

    def remove_message(self, message_id):
        pass

    def remove_chat(self, chat_id):
        pass

    def remove_contact(self, user_id, contact_name):
        if self.isincontacts(user_id, contact_name):
            return {'result': 'is_in_contact'}

    def edit_user_name(self, user_id, new_name):
        pass

    def edit_chat_name(self, chat_id, new_name):
        pass

    def get_user(self, user_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        user_name = [i for i in cur.execute(f'''SELECT name FROM Users WHERE id="{user_id}"''')]
        result = None
        if user_name != []:
            result = user_name[0][0]
        conn.close()
        return result

    def get_messages(self, user_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        chats_ids = self.get_chats_ids(user_id=user_id)
        result = []
        if not chats_ids is None:
            for chat_id in chats_ids:
                messages = [i for i in cur.execute(f'''SELECT id, chat_id, user_id, txt, time FROM Messages WHERE chat_id="{str(chat_id)}"''')]
                if messages != []:
                    for message in messages:
                        message = {'id': message[0], 'chat_id': message[1], 'user_id': message[2], 'text': message[3], 'time': message[4]}
                        result.append(message)
        conn.close()
        if result == []:
            result = None
        return result

    def get_contacts(self, user_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        contacts = [i for i in cur.execute(f'''SELECT users_id FROM Contacts WHERE user_id="{str(user_id)}"''')]
        result = None
        if contacts != []:
            result = contacts[0][0]
            result = result.split(' ')
        conn.close()
        return result

    def isincontacts(self, user_id, contact_id):
        contacts = self.get_contacts(user_id)
        if contacts is None:
            return False
        for contact in contacts:
            if int(contact) == int(contact_id):
                return True
        return False

    def get_chat_id(self, user1_id, user2_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        result = None
        for i in range(2):
            chat_id = [i for i in cur.execute(f'''SELECT id FROM Chats WHERE user1_id="{user1_id}" AND user2_id="{user2_id}"''')]
            if chat_id == [] and i == 0:
                user1_id, user2_id = user2_id, user1_id
                continue
            if chat_id != [] and i == 1 or chat_id != [] and i == 0:
                result = chat_id[0][0]
                break

        conn.close()
        return result

    def get_chats_ids(self, user_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        result = []
        for i in range(1, 3):
            chats_ids = [i for i in cur.execute(f'''SELECT id FROM Chats WHERE user{i}_id="{user_id}"''')]
            if chats_ids != []:
                for chat_id in chats_ids:
                    result.append(chat_id[0])
            elif i == 2 and result == []:
                result = None
        return result

    def get_contact_id(self, name):
        conn = self.connect_bd()
        cur = conn.cursor()
        user_id = [i for i in cur.execute(f'''SELECT id FROM Users WHERE name="{name}"''')]
        result = None
        if user_id != []:
            result = user_id[0][0]
        conn.close()
        return result

    def get_user_id(self, name, password):
        conn = self.connect_bd()
        cur = conn.cursor()
        user_id = [i for i in cur.execute(f'''SELECT id FROM Users WHERE name="{name}" AND password="{password}"''')]
        result = None
        if user_id != []:
            result = user_id[0][0]
        conn.close()
        return result

    def get_now_time(self):
        return datetime.now().strftime(self.dateformat)


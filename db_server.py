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
        time = datetime.now().strftime(self.dateformat)
        print(time)

        conn = self.connect_bd()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Users (id integer primary key,
                                                            name text)''')
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

    def add_user(self, name):
        if name == 'name':
            return False
        conn = self.connect_bd()
        cur = conn.cursor()
        user_id = self.get_user_id(name)
        if user_id is None:
            cur.execute('''INSERT INTO Users (name) VALUES ("''' + name + '")')
            conn.commit()
            result = True
        else:
            result = False
        conn.close()
        return result

    def add_message(self, chat_id, user_id, text):
        conn = self.connect_bd()
        cur = conn.cursor()
        cur.execute('''INSERT INTO Messages (chat_id, user_id, txt, time) VALUES (?, ?, ?, ?)''', (chat_id, user_id, text, ))
        conn.commit()
        conn.close()

    def add_chat_if_not_exist(self, user1_id, user2_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        chat_id = self.get_chat_id(user1_id, user2_id)
        result = None
        if chat_id is None:
            cur.execute('''INSERT INTO Chats (user1_id, user2_id) VALUES (?, ?)''', (user1_id, user2_id))
            conn.commit()
            result = self.get_chat_id(user1_id, user2_id)
        else:
            result = chat_id
        conn.close()
        return result


    def add_contact(self, user_id: int, contact_name: str):
        if contact_name == 'name':
            return {'result': 'is_not_exist'}
        need_add_contact_id = self.get_user_id(contact_name)
        contacts_id = self.get_contacts(user_id=user_id)

        if need_add_contact_id is None:
            return {'result': 'is_not_exist'}

        if self.isincontacts(user_id, need_add_contact_id):
            return {'result': 'is_in_contacts'}

        if need_add_contact_id == user_id:
            return {'result': 'is_your_name'}

        conn = self.connect_bd()
        cur = conn.cursor()

        if contacts_id is None:
            cur.execute('''INSERT INTO Contacts (user_id, users_id) VALUES (?, ?)''',
                        (user_id, str(need_add_contact_id)))
        else:
            contacts_id = contacts_id.split(' ')
            contacts_id.append(str(need_add_contact_id))
            contacts_id = ' '.join(contacts_id)
            cur.execute('''UPDATE Contacts SET users_id=? WHERE user_id=?''',
                        (contacts_id, user_id))
        conn.commit()
        conn.close()
        return {'result': 'ok'}

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
        user_name = [i for i in cur.execute('''SELECT name FROM Users WHERE id="''' + user_id + '"')]
        result = None
        if user_name != []:
            result = user_name[0][0]
        conn.close()
        return result

    def get_messages(self, user_id, last_time):
        pass

    def get_contacts(self, user_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        contacts = [i for i in cur.execute('''SELECT users_id FROM Contacts WHERE user_id="''' + str(user_id) + '"')]
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
            print(contact, contact_id)
            if int(contact) == int(contact_id):
                return True
        return False

    def get_chat_id(self, user1_id, user2_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        result = None
        for i in range(2):
            chat_id = [i for i in cur.execute('''SELECT id FROM Chats WHERE user1_id="''' + user1_id +
                                                 '" AND user2_id="' + user2_id + '"')]
            if chat_id == [] and i == 0:
                user1_id, user2_id = user2_id, user1_id
                continue
            if chat_id != [] and i == 1 or chat_id != [] and i == 0:
                result = chat_id[0][0]
                break

        conn.close()
        return result

    def get_user_id(self, name):
        conn = self.connect_bd()
        cur = conn.cursor()
        user_id = [i for i in cur.execute('''SELECT id FROM Users WHERE name="''' + name + '"')]
        result = None
        if user_id != []:
            result = user_id[0][0]
        conn.close()
        return result


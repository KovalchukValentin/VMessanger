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

    def connect_bd(self):
        return sqlite3.connect('VMessangerS.db')

    def add_user(self, name):
        conn = self.connect_bd()
        cur = conn.cursor()
        user_id = self.get_user_id(name)
        if user_id is None:
            cur.execute('''INSERT INTO Users (name) VALUES ("''' + name + '")')
            conn.commit()
            return True
        else:
            return False

    def add_message(self, chat_id, user_id, text):
        pass

    def add_chat(self, user1_id, user2_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        chat_id = self.get_chat_id(user1_id, user2_id)
        if chat_id is None:
            cur.execute('''INSERT INTO Chats (name) VALUES (?, ?)''', (user1_id, user2_id))
            conn.commit()
        else:
            return chat_id

    def add_contact(self, user_id, contact_name):

        if self.isincontacts(user_id, contact_name):
            return False
        contacts_id = self.get_contacts(user_id=user_id)

        conn = self.connect_bd()
        cur = conn.cursor()
        need_add_contact_id = str(self.get_user_id(contact_name))
        if contacts_id is None:
            cur.execute('''INSERT INTO Contacts (user_id, users_id) VALUES (?, ?)''',
                        (user_id, need_add_contact_id))
        else:
            contacts_id = contacts_id.split(' ')
            contacts_id.append(need_add_contact_id)
            contacts_id = ' '.join(contacts_id)
            cur.execute('''UPDATE Contacts SET users_id=? WHERE user_id=?''',
                        (contacts_id, user_id))
        conn.commit()
        return True

    def remove_message(self, message_id):
        pass

    def remove_chat(self, chat_id):
        pass

    def remove_contact(self, contact_id):
        pass

    def edit_user_name(self, user_id, new_name):
        pass

    def edit_chat_name(self, chat_id, new_name):
        pass

    def get_user(self, user_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        user_name = [i for i in cur.execute('''SELECT name FROM Users WHERE id="''' + user_id + '"')]
        if user_name == []:
            return None
        return user_name[0][0]

    def get_messages(self, user_id, last_time):
        pass

    def get_contacts(self, user_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        contacts = [i for i in cur.execute('''SELECT users_id FROM Contacts WHERE user_id="''' + str(user_id) + '"')]
        if contacts == []:
            return None
        return contacts[0][0]

    def isincontacts(self, user_id, contact_name):
        contacts = self.get_contacts(user_id)
        if contacts is None:
            return False
        for contact in contacts:
            current_name_contact = self.get_user(contact)
            if current_name_contact == contact_name:
                return True
        return False

    def get_chat_id(self, user1_id, user2_id):
        conn = self.connect_bd()
        cur = conn.cursor()
        for i in range(2):
            chat_id = [i for i in cur.execute('''SELECT id FROM Chats WHERE user1_id="''' + user1_id +
                                                 '" AND user2_id="' + user2_id + '"')]
            if chat_id == [] and i == 0:
                user1_id, user2_id = user2_id, user1_id
                continue
            elif chat_id == [] and i == 1:
                return None
            return chat_id[0][0]

    def get_user_id(self, name):
        conn = self.connect_bd()
        cur = conn.cursor()
        user_id = [i for i in cur.execute('''SELECT id FROM Users WHERE name="''' + name + '"')]
        if user_id == []:
            return None
        return user_id[0][0]

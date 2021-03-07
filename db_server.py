import sqlite3

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
        self.conn = sqlite3.connect('VMessangerS.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Users (id integer primary key,
                                                            name text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS Messages (id integer primary key,
                                                               chat_id integer,
                                                               user_id integer,
                                                               txt text, 
                                                               time text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS Chats (id integer primary key,
                                                            user1_id integer,
                                                            user2_id integer)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS Contacts (id integer primary key,
                                                               user_id integer,
                                                               users_id text)''')
        self.conn.commit()

    def add_user(self):
        pass

    def add_message(self):
        pass

    def add_chat(self):
        pass

    def add_contact(self):
        pass

    def remove_message(self):
        pass

    def remove_chat(self):
        pass

    def remove_contact(self):
        pass

    def edit_user_name(self):
        pass

    def edit_chat_name(self):
        pass

    def get_user(self):
        pass

    def get_messages(self, ):
        pass

    def get_chat(self):
        pass

    def get_contacts(self):
        pass

import sqlite3

# User
# user_id
# last_time

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('VMessangerC.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS User (id integer,
                                                           name text,
                                                           last_time text)''')

    def save_user_if_not_exists(self, user_id: int, user_name: str, last_time: str):
        if self.get_user() == None:
            self.c.execute('''INSERT INTO User (id, name, last_time) VALUES (?, ?, ?)''',
                           (user_id, user_name, last_time))
        else:
            self.c.execute('''UPDATE User SET last_time=?, name=? WHERE id=?''',
                           (last_time, user_name, user_id))
        self.conn.commit()

    def get_user(self):
        user = [i for i in self.c.execute('''SELECT id, name, last_time FROM User''')]
        if user == []:
            return None
        return {'user_id': user[0][0], 'user_name': user[0][1], 'last_time': user[0][2]}

    def remove_user(self):
        self.c.execute('''DELETE From User''')
        self.conn.commit()
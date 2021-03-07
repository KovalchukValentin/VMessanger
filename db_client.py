import sqlite3

# User
# user_id
# last_time

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('VMessangerC.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS User (id integer,
                                                           last_time text)''')

    def save_user_if_not_exists(self, user_id: int, last_time: str):
        if self.get_user() == None:
            self.c.execute('''INSERT INTO User (id, last_time) VALUES (?, ?)''',
                           (user_id, last_time))
        else:
            self.c.execute('''UPDATE User SET last_time=? WHERE id=?''',
                           (last_time, user_id))
        self.conn.commit()

    def get_user(self):
        user = [i for i in self.c.execute('''SELECT id, last_time FROM User''')]
        if user == []:
            return None
        return user[0][0]

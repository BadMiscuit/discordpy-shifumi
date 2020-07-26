import sqlite3

class DbConnection:
    def __init__(self):
        pass

    def __enter__(self):
        self.conn = sqlite3.connect('srs-discordbot.db')
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        try:
            self.conn.commit()
        except Exception as e:
            print(str(e))
            self.conn.rollback()
        self.conn.close()


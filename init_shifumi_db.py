import sqlite3

conn = sqlite3.connect('srs-discordbot.db')

c = conn.cursor()

c.execute ('DROP TABLE IF EXISTS score')
c.execute('''
        CREATE TABLE score(
        id VARCHAR PRIMARY KEY,
        username VARCHAR,
        user_score INTEGER,
        bot_score INTEGER)
        ''')

conn.commit()

conn.close()


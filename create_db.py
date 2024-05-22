import sqlite3

conn = sqlite3.connect('library.db')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        year TEXT NOT NULL,
        edition_id TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

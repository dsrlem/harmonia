import sqlite3

conn = sqlite3.connect('library.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    year INTEGER NOT NULL,
    edition_id INTEGER NOT NULL
)
''')

conn.commit()
conn.close()

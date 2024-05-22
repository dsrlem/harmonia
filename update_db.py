import sqlite3

conn = sqlite3.connect('library.db')
cur = conn.cursor()


cur.execute("PRAGMA table_info('books')")
columns = cur.fetchall()
column_names = [col[1] for col in columns]
if 'edition_id' not in column_names:

    cur.execute("ALTER TABLE books ADD COLUMN edition_id TEXT NOT NULL DEFAULT ''")

conn.commit()
conn.close()

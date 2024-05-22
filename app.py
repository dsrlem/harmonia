from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'library.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        edition_id = request.form['edition_id']
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, genre, year, edition_id) VALUES (?, ?, ?, ?, ?)', (title, author, genre, year, edition_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        edition_id = request.form['edition_id']
        cur.execute('UPDATE books SET title = ?, author = ?, genre = ?, year = ?, edition_id = ? WHERE id = ?', (title, author, genre, year, edition_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM books WHERE id = ?', (id,))
    book = cur.fetchone()
    conn.close()
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:id>')
def delete_book(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
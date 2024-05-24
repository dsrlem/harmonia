import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import dj_database_url

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///library.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def get_db():
    conn = sqlite3.connect('library.db')
    return conn

@app.route('/')
def index():
    search_query = request.args.get('search')
    conn = get_db()
    cur = conn.cursor()
    if search_query:
        cur.execute("""
            SELECT * FROM books 
            WHERE id LIKE ? 
            OR title LIKE ? 
            OR author LIKE ? 
            OR genre LIKE ? 
            OR year LIKE ?""",
                    ('%' + search_query + '%',
                     '%' + search_query + '%',
                     '%' + search_query + '%',
                     '%' + search_query + '%',
                     '%' + search_query + '%'))
    else:
        cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    conn.close()
    return render_template('index.html', books=books, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        edition_id = request.form['edition_id']

        # Validate that year is a number
        if not year.isdigit():
            error = "Ano deve ser um número."
            return render_template('add_book.html', error=error)

        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, genre, year, edition_id) VALUES (?, ?, ?, ?, ?)',
                    (title, author, genre, year, edition_id))
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

        if not year.isdigit():
            error = "Ano deve ser um número."
            cur.execute('SELECT * FROM books WHERE id = ?', (id,))
            book = cur.fetchone()
            conn.close()
            return render_template('edit_book.html', book=book, error=error)

        cur.execute('UPDATE books SET title = ?, author = ?, genre = ?, year = ?, edition_id = ? WHERE id = ?',
                    (title, author, genre, year, edition_id, id))
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

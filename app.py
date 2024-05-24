import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///library.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255))
    year = db.Column(db.Integer)
    edition_id = db.Column(db.Integer)

@app.route('/')
def index():
    search_query = request.args.get('search')
    if search_query:
        books = Book.query.filter(
            db.or_(
                Book.id.like('%{}%'.format(search_query)),
                Book.title.like('%{}%'.format(search_query)),
                Book.author.like('%{}%'.format(search_query)),
                Book.genre.like('%{}%'.format(search_query)),
                Book.year.like('%{}%'.format(search_query))
            )
        ).all()
    else:
        books = Book.query.all()
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

        book = Book(title=title, author=author, genre=genre, year=year, edition_id=edition_id)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        edition_id = request.form['edition_id']

        if not year.isdigit():
            error = "Ano deve ser um número."
            return render_template('edit_book.html', book=book, error=error)

        book.title = title
        book.author = author
        book.genre = genre
        book.year = year
        book.edition_id = edition_id

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

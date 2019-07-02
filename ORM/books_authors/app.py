from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
app = Flask(__name__)

# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_author.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)

details_table =db.Table('details',
              db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True),
              db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True))

genres_table = db.Table('genres',
              db.Column('genre_id', db.Integer, db.ForeignKey('genre_list.id'), primary_key=True),
              db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True))
# the db.Model in parentheses tells SQLAlchemy that this class represents a table in our database
class Book(db.Model):
    __tablename__ = "books"    # optional
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    publication_year = db.Column(db.Integer())
    genres_this_book_has = db.relationship('Genre', secondary=genres_table)
    authors_this_book_has = db.relationship('Author', secondary=details_table)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    notes = db.Column(db.Text)
    books_this_author_has = db.relationship('Book', secondary=details_table)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Genre(db.Model):
    __tablename__ = "genre_list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    books_this_genre_has = db.relationship('Book', secondary=genres_table)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


@app.route('/')
def index():
    all_books = Book.query.all()
    all_authors = Author.query.all()
    all_genres = Genre.query.all()
    return render_template('index.html', books=all_books, authors=all_authors, genres=all_genres)

@app.route('/create-genre', methods=['POST'])
def create_genre():
    new_genre = Genre(name=request.form['name'])
    db.session.add(new_genre)
    db.session.commit()

@app.route('/create-author', methods=['POST'])
def create_author():
    new_author = Author(first_name=request.form['first_name'],
                    last_name=request.form['last_name'], notes=request.form['notes'])
    db.session.add(new_author)
    db.session.commit()
    if request.form['button_type'] == "authors_page":
        return redirect('/authors')
    return redirect('/')


@app.route('/create-book', methods=['POST'])
def create_book():
    added_genre = Genre.query.get(request.form['genre_id'])
    new_book = Book(name=request.form['name'], description=request.form['description'],
                    publication_year=request.form['publication_year'])
    new_book.genres_this_book_has.append(added_genre)
    db.session.add(new_book)
    db.session.commit()
    if request.form['button_type'] == "books_page":
        return redirect('/books')
    return redirect('/')


@app.route('/books/<id>')
def show_book(id):
    view_book = Book.query.get(id)
    all_authors = Author.query.all()
    all_genres = Genre.query.all()
    return render_template('book_details.html', book=view_book, authors=all_authors, genres=all_genres)


@app.route('/books/<id>/edit', methods=['POST'])
def edit_book(id):
    if request.form['button_type'] == 'author':
        book = Book.query.get(id)
        author = Author.query.get(request.form['author_id'])
        book.authors_this_book_has.append(author)
        db.session.commit()
    else:
        book = Book.query.get(id)
        genre = Genre.query.get(request.form['genre_id'])
        book.genres_this_book_has.append(genre)
        db.session.commit()
    return redirect('/books/{}'.format(id))

@app.route('/authors/<id>/edit', methods=['POST'])
def edit_author(id):
    if request.form['button_type'] == 'book':
        author = Author.query.get(id)
        book = Book.query.get(request.form['book_id'])
        author.books_this_author_has.append(book)
        db.session.commit()
    return redirect('/authors/{}'.format(id))

@app.route('/books')
def show_books():
    all_books = Book.query.all()
    all_genres = Genre.query.all()
    return render_template('books.html', books=all_books, genres=all_genres)


@app.route('/authors')
def show_authors():
    all_authors = Author.query.all()
    return render_template('authors.html', authors=all_authors)

@app.route('/authors/<id>')
def show_author(id):
    view_author = Author.query.get(id)
    all_books = Book.query.all()
    return render_template('author_details.html', author=view_author, books=all_books)

if __name__ == "__main__":
    app.run(debug=True)
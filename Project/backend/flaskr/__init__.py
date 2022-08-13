import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
from models import Book

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    format_books = [book.format() for book in selection]
    return format_books[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/")
    def index():
        return "Book Home"

    #To get all books
    @app.route("/books")
    def get_books():
        selection = Book.query.order_by(Book.id).all()
        #Access paginate method to filter out books on basis of page selected
        books = paginate(request, selection)

        if len(books) == 0 :
            abort(404)
       
        return jsonify({"books": books, "total_books": len(selection), "success": True})

     #To get specified book
    @app.route("/books/<int:book_id>")
    def view_book(book_id):
        book = Book.query.filter(Book.id == book_id).one_or_none()
        if book is None :
            abort(404)
       
        return jsonify({"books": book.format(), "success": True})

    @app.route('/books/edit/<int:book_id>',methods=['PATCH'])
    def update_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None :
                abort(404)
            else:
                body = request.get_json()
                #As we are only allowing rating column to be modified
                if 'rating' in body:
                    book.rating = int(body.get('rating'))
                book.update()
                return jsonify({
                    'id':book.id,
                    'success':True
                })
        except:
            abort(500)

    return app

import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Book

class BookTestCase(unittest.TestCase):
    def setUp(self):
        #Initialize the flask app
        self.app = create_app()

        #Initialize the client to access local context via its context manager
        self.client = self.app.test_client

        #Setup test database
        self.database = "postgresql://student:student@localhost:5432/bookshelf_test"
        setup_db(self.app,self.database)

        self.new_book = {"title": "The Great Alone", "author": "Kristin Hannah", "rating": 5}

    def tearDown(self):
        #We do not need anything to be undone for this app as of now
        pass

    def test_get_books(self):
        res = self.client().get('http://127.0.0.1:5000/books')
        #Load the data
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_404_page_beyond_limit(self):
        res = self.client().get('/books?page=10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not found')

    def test_updating_book(self):
        res = self.client().patch("/books/edit/1",json={'rating':1})
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(book.format()['rating'],1)

    def test_updating_book_without_data(self):
        res = self.client().patch("/books/edit/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        #self.assertEqual(data['success'],False)

if __name__ == "__main__":
    unittest.main()
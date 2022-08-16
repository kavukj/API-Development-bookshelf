import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db

class BookTestCase(unittest.TestCase):
    def setUp(self):
        #Initialize the flask app
        self.app = create_app()

        #Initialize the client to access local context via its context manager
        self.client = self.app.test_client()

        #Setup test database
        self.database = "postgresql://student:student@localhost:5432/bookshelf_test"
        setup_db(self.app,self.database)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

    def tearDown(self):
        #We do not need anything to be undone for this app as of now
        pass

    def test_get_books(self):
        res = self.client().get('/books')
        #Load the data
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

if __name__ == "main":
    print("called")
    unittest.main()
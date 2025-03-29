import unittest
import os
from unittest.mock import patch, MagicMock
from website.verseus import Verse_Test
from website import create_app, db
from website.models import User, Note

class TestVerseTest(unittest.TestCase):
    # def setUp(self):
    #     self.app = create_app()
    #     self.app.config['TESTING'] = True
    #     self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    #     self.client = self.app.test_client()
    #     self.ctx = self.app.app_context()
    #     self.ctx.push()
    #     db.create_all()

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.ctx.pop()

    def test_verse_storage(self):
        # Create test data
        test_verse = "John 3:16"
        test_completion = "For God so loved the world"
        
        # Initialize Verse_Test instance
        verse_test = Verse_Test()
        with create_app.app_context():
            a = Note.query.filter_by(user_id=1, id=1).first()
        # Test storing verse and completion
        verse_test.verse = a.data
        verse_test.completion = a.completions
        
        # Verify values are stored correctly
        self.assertEqual(verse_test.verse, "a a a a ")
        self.assertEqual(verse_test.completion, test_completion)

if __name__ == '__main__':
    unittest.main() 
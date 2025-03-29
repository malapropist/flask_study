import unittest
import os
from unittest.mock import patch, MagicMock
from website.verseus import Verse_Test
from website import create_app, db
from website.models import User, Note

class TestVerseTest(unittest.TestCase):
    def setUp(self):
        # Create app with existing database
        self.app = create_app()
        self.app.config['TESTING'] = True
        # Use the existing database file
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_verse_storage(self):
        # Get existing data from database
        with self.app.app_context():
            a = Note.query.filter_by(user_id=1, id=1).first()
            u = User.query.filter_by(id=1).first()
            
            # Test storing verse and completion
            verse_test = Verse_Test(u, 1)
            verse_test.verse = a.data
            verse_test.completion = a.completions
            print(verse_test.verse)
            print(verse_test.completion)

            # Verify values are stored correctly
            self.assertEqual(verse_test.verse, "a a a")
            self.assertEqual(verse_test.completion, 0)
            self.assertEqual(verse_test.word_blank_positions, [0,0,0])

    def test_check_answer(self):
        with self.app.app_context():
            a = Note.query.filter_by(user_id=1, id=1).first()
            u = User.query.filter_by(id=1).first()
            
            verse_test = Verse_Test(u, 1)
            verse_test.verse = a.data
            verse_test.completion = a.completions

            verse_test.check_answer("a a a")
            
            # Refresh the note from database to see changes
            db.session.refresh(a)
            a = Note.query.filter_by(user_id=1, id=1).first()

            print(f"Completions after check_answer: {a.completions}")
            print(f"Word blank positions after check_answer: {a.word_blank_positions}")

            self.assertEqual(a.completions, 1)
            self.assertEqual(sum(a.word_blank_positions), 1)

if __name__ == '__main__':
    unittest.main() 
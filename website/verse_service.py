from .models import Note
from . import db
from flask import current_app
from website import create_app

class VerseService:
    @staticmethod
    def get_note(user_id, note_id):
        return Note.query.filter_by(user_id=user_id, id=note_id).first()

    @staticmethod
    def update_note_completions(note_id, completions):
        note = Note.query.filter_by(user_id=1, id=note_id).first()
        if note:
            note.completions = completions
            print("note completions: ", note.completions)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_verse_data(user_id, note_id) -> tuple[str, str, int, list[int]]:

        note = Note.query.filter_by(user_id=user_id, id=note_id).first()
        if note:
            return note.data, note.ref, note.completions, note.word_blank_positions
        return "", "", 0, []
    
    @staticmethod
    def update_verse_blanks(note_id, word_blank_positions):
        note = Note.query.filter_by(user_id=1, id=note_id).first()
        if note:
            note.word_blank_positions = word_blank_positions
            db.session.commit()
            return True
        return False
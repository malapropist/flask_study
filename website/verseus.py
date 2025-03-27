import random

from .models import Note
from flask_login import current_user

class Verse_Test:

    def __init__(self, current_user=None, note_id=None, completions=0):
        self.letter_scores = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1,
            'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 5,
            'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1,
            'P': 3, 'Q': 6, 'R': 1, 'S': 1, 'T': 1,
            'U': 1, 'V': 4, 'W': 4, 'X': 5, 'Y': 4,
            'Z': 6
        }
        self.word_blank_positions = []
        self.potential_score = 0
        self.verse, self.reference = self.get_verse_from_db(current_user.id, note_id)
        self.completions = completions
        
        if self.verse:
            self.verse_list = self.verse.split(" ")
            self.verse_word_length = len(self.verse_list)
            self.word_blank_positions = [0 for _ in range(self.verse_word_length)]
            self.blanks_inserted_verse = self.gen_new_blanks()

    # Get verse and reference from database based on user ID and note ID
    def get_verse_from_db(self, user_id, note_id):
        note = Note.query.filter_by(user_id=user_id, id=note_id).first()
        if note:
            return note.data, note.ref
        return None, None

    @staticmethod
    def score_word(word, scores_matrix):
        return sum([scores_matrix[letter] for letter in word.upper()])

    def gen_new_blanks(self):
        # Generate new blanks based on completions
        for new_blank_spot in random.sample(range(0, self.verse_word_length), 
                                          min(self.completions, self.verse_word_length)):
            self.word_blank_positions[new_blank_spot] = 1
            self.potential_score += self.score_word(self.verse_list[new_blank_spot], 
                                                  self.letter_scores)
        # send retrn based on verse_list parallel with word blanks calc the new verse with blanks
        return [self.verse_list[i] if self.word_blank_positions[i] == 0 
                else "_" * len(self.verse_list[i]) 
                for i in range(self.verse_word_length)]

    def check_answer(self, user_answer):
        if not user_answer:
            return 0, 0, "Please provide an answer"

        resp_list = user_answer.split(" ")
        if len(resp_list) != self.verse_word_length:
            return 0, 0, "Answer must have the same number of words as the verse"

        current_score = 0
        correct_words = []
        for spot in range(self.verse_word_length):
            if resp_list[spot].upper() == self.verse_list[spot].upper() and self.word_blank_positions[spot] == 1:
                current_score += self.score_word(resp_list[spot], self.letter_scores)
                correct_words.append(spot)

        if current_score == self.potential_score:
            message = f"Perfect! You've earned {current_score} points!"
        else:
            message = f"Good try! You've earned {current_score} points. Keep practicing!"

        return current_score, self.potential_score, message

    def get_verse_display(self):
        return " ".join(self.blanks_inserted_verse)

    def get_verse_info(self):
        return {
            'verse': self.get_verse_display(),
            'reference': self.reference,
            'potential_score': self.potential_score,
            'word_count': self.verse_word_length
        }
    
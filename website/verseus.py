import random
from .verse_service import VerseService

class Verse_Test:

    def __init__(self, current_user=None, note_id=None):
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
        self.current_user = current_user
        self.note_id = note_id
        self.verse = "a a a"
        self.reference = None
        self.completions = 0
        
        # Get verse data through service layer
        if current_user and note_id:
            self.verse, self.reference, self.completions, self.word_blank_positions = VerseService.get_verse_data(
                current_user.id, note_id)
        if self.verse:
            self.verse_list = self.verse.split(" ")
            self.verse_word_length = len(self.verse_list)
        if self.verse and not self.word_blank_positions:
            self.word_blank_positions = [0 for _ in range(self.verse_word_length)]
        self.blanks_inserted_verse = self.gen_new_blanks()

    @staticmethod
    def score_word(word, scores_matrix):
        total = sum([scores_matrix[letter] if letter in scores_matrix else 0 for letter in word.upper()])
        return total

    def gen_new_blanks(self):
        # Generate new blanks based on completions
        # Get indices where word_blank_positions is 0
        new_blank_spots = []
        available_spots = [i for i in range(self.verse_word_length) if self.word_blank_positions[i] == 0]
        # Sample from available spots only
        num_new_blanks = min(self.completions, len(available_spots))
        if num_new_blanks > 0:  # Only sample if we have spots available
            new_blank_spots = random.sample(available_spots, num_new_blanks)
        for new_blank_spot in new_blank_spots:
            self.word_blank_positions[new_blank_spot] = 1
        for blank_flag in self.word_blank_positions:
            if self.word_blank_positions[blank_flag] == 1:
                self.potential_score += self.score_word(self.verse_list[blank_flag], self.letter_scores)
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
            print(message)
            # Update completions through service layer
            if self.current_user and self.note_id:
                print("Writing completions to database")
                VerseService.update_note_completions(self.note_id, self.completions+1)
                print("new completions: ", VerseService.get_verse_data(self.current_user.id, self.note_id)[2])
                print("Updating verse blanks")
                VerseService.update_verse_blanks(self.note_id, self.word_blank_positions)
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
    
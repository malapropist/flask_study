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

        # Initialize base verse data
        self.word_blank_positions = []
        self.potential_score = 0
        self.current_user = current_user
        self.note_id = note_id
        self.verse = "a a a"
        self.reference = None
        self.completions = 0
        self.blanks_inserted_verse = ""
        self.verse_list = []
        self.verse_word_length = 0
        self.sum_of_blanks = 0
        

        # Get verse data through service layer
        if current_user and note_id:
            self.verse, self.reference, self.completions, self.word_blank_positions = VerseService.get_verse_data(current_user.id, note_id)
        if self.verse:
            self.verse_list = self.verse.split(" ")
            self.verse_word_length = len(self.verse_list)
        else:
            print("Error: verse is not set")

        if not self.word_blank_positions or len(self.word_blank_positions) == 0:
            self.word_blank_positions = [0 for _ in range(self.verse_word_length)]
        
        # count the number of blanks in the verse
        self.sum_of_blanks = sum(self.word_blank_positions)
        
        if not self.sum_of_blanks or self.sum_of_blanks == 0:
            self.blanks_inserted_verse = self.verse
        elif self.sum_of_blanks < self.completions:
            self.word_blank_positions = self.gen_new_blanks()
            self.blanks_inserted_verse = self.format_old_blanks(self.word_blank_positions)
        elif self.sum_of_blanks == self.completions:
            self.blanks_inserted_verse = self.format_old_blanks(self.word_blank_positions)
        else:
            print("Error: sum_of_blanks is greater than the number of completions")
            self.completions = self.sum_of_blanks
            self.blanks_inserted_verse = self.format_old_blanks(self.word_blank_positions)
        if self.word_blank_positions:
            self.potential_score = self.calculate_potential_score()


    @staticmethod
    def score_word(word, scores_matrix):
        total = sum([scores_matrix[letter] if letter in scores_matrix else 0 for letter in word.upper()])
        return total

    def calculate_potential_score(self):
        potential_score = 0
        for i, blank_flag in enumerate(self.word_blank_positions):
            if blank_flag == 1:
                potential_score += self.score_word(self.verse_list[i], self.letter_scores)
        return potential_score

    def format_old_blanks(self, word_blank_positions):
        return " ".join([self.verse_list[i] if word_blank_positions[i] == 0 else "_" * len(self.verse_list[i]) for i in range(self.verse_word_length)])

    def gen_new_blanks(self):
        print("Generating new blanks...")
        n_new_blanks = min(self.completions+1, self.verse_word_length) - self.sum_of_blanks
        new_blank_spots = []
        # Get indices where word_blank_positions is 0
        print(self.word_blank_positions, self.verse_word_length)
        available_spots = [i for i in range(self.verse_word_length) if self.word_blank_positions[i] == 0]
        if len(available_spots) > 0 and n_new_blanks > 0:
            # pick a number_new_blanks of random spots from available_spots
            new_blank_spots = random.sample(available_spots, n_new_blanks)
        
        w_blank_positions = self.word_blank_positions
        for new_blank_spot in new_blank_spots:
            w_blank_positions[new_blank_spot] = 1
        print("Generated new blank(s) at: ", w_blank_positions)

        return w_blank_positions

    def update_completions(self, new_blanks):
        if self.current_user and self.note_id:
            print("Writing completions to database...")
            success = VerseService.update_note_completions(self.note_id, self.completions+1)
            if success:
                print("Successfully updated completions")
            else:
                print("Error updating completions")

            print("Updating verse blanks...")
            print("current word_blank_positions: ", self.word_blank_positions)
            success = VerseService.update_verse_blanks(self.note_id, new_blanks)
            if success:
                print("Successfully updated verse blanks")
                print("new word_blank_positions: ", VerseService.get_verse_data(self.current_user.id, self.note_id)[3])
            else:
                print("Error updating verse blanks")
        else:
            print("Error writing completions to database: no current user or note id")


    def check_answer(self, user_answer):
        if not user_answer:
            return 0, -1, "Please provide an answer"

        resp_list = user_answer.split(" ")
        if len(resp_list) != self.verse_word_length:
            return 0, -1, "Answer must have the same number of words as the verse"

        current_score = 0
        correct_words = []
        for spot in range(self.verse_word_length):
            if resp_list[spot].upper() == self.verse_list[spot].upper() and self.word_blank_positions[spot] == 1:
                current_score += self.score_word(resp_list[spot], self.letter_scores)
                correct_words.append(spot)
            elif resp_list[spot].upper() != self.verse_list[spot].upper() and self.word_blank_positions[spot] == 0:
                current_score -= 1
        self.potential_score = self.calculate_potential_score()
        if current_score == self.potential_score:
            message = f"Perfect! You've earned {current_score} points!"
            # Update completions through service layer
            new_blanks = self.gen_new_blanks()
            self.update_completions(new_blanks)
        else:
            message = f"Good try! You've earned {current_score} points. Keep practicing!"
        print("current_score: ", current_score, "potential_score: ", self.potential_score, "message: ", message)
        return current_score, self.potential_score, message

    def get_verse_display(self):
        return " ".join(self.blanks_inserted_verse)

    def get_verse_info(self):
        return {
            'verse': self.blanks_inserted_verse,
            'reference': self.reference,
            'potential_score': self.potential_score,
            'word_count': self.verse_word_length,
            'word_blank_positions': self.word_blank_positions
        }
    
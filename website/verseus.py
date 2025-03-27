import random

# Usually this will be passed from server or enter new verse
verse = """For God so loved the world that He gave his only begotten son"""
# TODO Source from dictionary of all verses and chapters
reference = ["John","3","16"]


class Verse_Test:

    def __init__(self, verse=verse,reference=reference,completions=0):
        self.letter_scores = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1,
        'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 5,
        'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1,
        'P': 3, 'Q': 6, 'R': 1, 'S': 1, 'T': 1,
        'U': 1, 'V': 4, 'W': 4, 'X': 5, 'Y': 4,
        'Z': 6
    }
        self.verse = verse
        verse_list = verse.split(" ")
        verse_word_length = len(verse_list)
        self.reference = reference
        self.completions = completions
        # Pull these from server
        word_blank_positons = [0 for i in range(verse_word_length)]
        potential_score = 0

        

    def score_word(word, scores_matrix):
        score = sum([scores_matrix[letter] for letter in word.upper()])
        return score
    
    
    
    def gen_new_blanks(self, verse_word_length,completions,word_blank_positons,score_word,verse_list,letter_scores):
        # Generate new blanks locally, to be pushed along with everything else
        for new_blank_spot in random.sample(range(0,verse_word_length), min(completions,verse_word_length)):
            word_blank_positons[new_blank_spot]=1
            potential_score += score_word(verse_list[new_blank_spot],letter_scores)

        blanks_inserted_verse = [verse_list[i] if word_blank_positons[i]==0 else "_"*len(verse_list[i]) for i in range(verse_word_length)]

        return blanks_inserted_verse
    
    def receive_text(self, verse_word_length,completions,potential_score,blanks_inserted_verse,verse_list,word_blank_positons,letter_scores):
        
        # contain the score, length, and word
        verse_list_dict = {(0)}
        
        print("Complete the verse!\n")
        print(verse_word_length, completions, potential_score)
        resp = input(" ".join(blanks_inserted_verse)+"\n")
        if resp == verse:
            print(f"Pass! You have added {potential_score} to your total Verseus score for the week!")
        else:
            resp_list = resp.split(" ")
            current_score = 0
            for spot in range(verse_word_length):
                if resp_list[spot] == verse_list[spot] and word_blank_positons[spot] == 1:
                    current_score += self.score_word(resp_list[spot],letter_scores)
            print(f"Nice try. At least you still added {current_score} to your total Verseus score for the week!")

        return (current_score, potential_score)
    
from collections import defaultdict

def run_game():
    
    # ask the player to input the length of word
    while True:
        try: word_length = int(input("Please input the length of word: "))
        # except ValueError: print("Please enter an integer")
        except ValueError: pass
        else: break
    
    my_word_maker = word_maker()
    my_word_maker.reset(word_length)
    
    # print (f"Amount of valid words is: {my_word_maker.get_amt_valid_words()}.")

    num_guessed = 0
    max_guess = 5
    display = ["-"] * word_length
    while num_guessed < max_guess:
        guess_letter = input("Please input your guess letter: ")

        final_pos = my_word_maker.guess (guess_letter)
        # print (my_word_maker.position_dict)

        for i in final_pos:
            display[i] = guess_letter
        display_word = ''.join(display)
        print(f"The word is: {display_word}")

        if '-' in display:
            num_guessed += 1
            print(f"Number of guess left is: {max_guess - num_guessed}")
            if max_guess - num_guessed == 0:
                print("You lost!")
                break
        else:
            print("You won!")
            break

    # get valid word
    # valid_word = position_dict[position][0]
    valid_word = None
    for position, words in my_word_maker.position_dict.items():
        valid_word = words[0]
    print(f"The word was: {valid_word}!")

class word_maker():
    # init function
    def __init__(self):
        self.words = {}
        with open("dictionary.txt") as file_obj:
            for line in file_obj:
                word = line.strip()
                if len(word) > 0:
                    self.words[word] = len(word)
        self.words_init = self.words

    # reset function
    def reset(self, word_length):
        self.words = {word: length for word, length in self.words_init.items() if length == word_length}
        # words = [word for word, length in words.items() if length == word_length]
        # print(f"Dict of words with the given length is: {words}")

    # get amount of valid words function
    def get_amt_valid_words (self):
        return len(self.words)

    # get letter position in word
    def get_letter_position (word, guess_letter):
        result = []

        idx = word.find(guess_letter)
        while idx != -1:
                result.append(idx)
                idx = word.find(guess_letter, idx + 1)

        return (tuple(result))

    # guess function
    def guess (self, guess_letter):
        self.position_dict = defaultdict(list)
        for word in self.words:
            position = word_maker.get_letter_position(word, guess_letter)
            self.position_dict[position].append(word)
        # print(position_dict)

        max_len = 0
        max_key_list = []
        for position, words in self.position_dict.items():
            if len(words) > max_len:
                max_len = len(words)
                max_key_list = [position]
            elif len(words) == max_len:
                max_key_list.append(position)
        # print(f"Max position list is: {max_key_list}")

        min_letters = float('inf')
        final_key = None
        for position in max_key_list:
            if len(position) < min_letters:
                min_letters = len(position)
                final_key = position
        # print(f"Final position is: {final_key}")     

        self.position_dict = {position: words for position, words in self.position_dict.items() if position == final_key}
        #words = {word: length for word, length in words.items() if len(word) == max_len}
        # print(position_dict)

        self.words = {word: len(word) for word in self.position_dict[final_key]}
        # print(f"Updated words dict is: {words}")

        final_pos = list(final_key)
        return final_pos

run_game()
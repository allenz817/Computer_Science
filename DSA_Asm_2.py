from collections import defaultdict

# get letter position in word
def get_letter_position (word, guess_letter):
    result = []

    idx = word.find(guess_letter)
    while idx != -1:
            result.append(idx)
            idx = word.find(guess_letter, idx + 1)

    return (tuple(result))

# init function
words = {}
with open("dictionary.txt") as file_obj:
    for line in file_obj:
        word = line.strip()
        if len(word) > 0:
            words[word] = len(word)
words_init = words

word_length = int(input("Please input the length of word: "))
# word_length = 5

# reset function
words = {word: length for word, length in words_init.items() if length == word_length}
# words = [word for word, length in words.items() if length == word_length]
# print(f"Dict of words with the given length is: {words}")

# get amount of valid words function
print(f"Amount of valid words is: {len(words)}")

guess_letter = input("Please input your guess letter: ")
# guess_letter = "l"

# guess function
position_dict = defaultdict(list)
for word in words:
     position = get_letter_position(word, guess_letter)
     position_dict[position].append(word)
# print(position_dict)
#"""

max_len = 0
max_key_list = []
for position, words in position_dict.items():
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

position_dict = {position: words for position, words in position_dict.items() if position == final_key}
#words = {word: length for word, length in words.items() if len(word) == max_len}
# print(position_dict)

final_pos = list(final_key)
# print(final_pos)

words = {word: len(word) for word in position_dict[final_key]}
# print(f"Updated words dict is: {words}")

# get valid word
# valid_word = position_dict[position][0]
for position, words in position_dict.items():
     valid_word = words[0]
print(f"The word is: {valid_word}!")
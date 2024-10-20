import random
import typing
from typing import Optional, Dict, Set, List, Tuple
from collections.abc import Iterator

class TrieNode:
    """
    Our TrieNode class. Feel free to add new properties/functions, but 
    DO NOT edit the names of the given properties (children and is_word).
    """
    def __init__(self):
        self.children : Dict[str, TrieNode] = {} # maps a child letter to its TrieNode class
        self.is_word = False # whether or not this Node is a valid word ending


class TrieDictionary():
    """
    Your implementation of BoggleDictionary.
    Several functions have been filled in for you from our solution, but you are free to change their implementations.
    Do NOT change the name of self.root, as our autograder will manually traverse using self.root
    """

    def __init__(self):
        self.root : TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        # Remember to add every word to the trie, not just the words over some length.
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()
                # Do something with word here
                node = self.root
                for char in word:
                    if char not in node.children:
                        node.children[char] = TrieNode()
                    node = node.children[char]
                node.is_word = True
                
    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """
        Traverse will traverse the Trie down a given path of letters `prefix`.
        If there is ever a missing child node, then returns None.
        Otherwise, returns the TrieNode referenced by `prefix`.
        """
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def contains(self, word: str) -> bool:
        node = self.traverse(word.lower())
        return (node is not None) and node.is_word
        """
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return True
        """
          
# read words file
WORDS_FILE = "words.txt"
words: Set[str] = set()
with open(WORDS_FILE, "r") as fin:
    for line in fin:
        line = line.strip().upper()
        words.add(line)

game_dict = TrieDictionary()
game_dict.load_dictionary(WORDS_FILE)

def test_contains_all_example():
    for s in words:
        assert game_dict.contains(s)
        
test_contains_all_example()

# print(game_dict.contains("becap")) -> returns True

SHORT = 3
CUBE_SIDES = 6
      
class MyGameManager():
    def __init__(self):
        self.board: List[List[str]] # current game board
        self.size: int # board size
        self.words: List[str] # player's current words
        # self.dictionary: BoggleDictionary # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] # the position of the last added word, or None

    # def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
    def new_game(self, size: int, cubefile: str) -> None:
        with open(cubefile, 'r') as infile:
            faces = [line.strip() for line in infile]
        cubes = [f.lower() for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size*size:
            raise ValueError('ERROR: Invalid Dimensions (size, cubes)')
        random.shuffle(cubes)
        # Set all of the game parameters
        self.board =[[random.choice(cubes[r*size + c]) 
                    for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        # self.dictionary = dictionary
        self.last_added_word = None

    def get_board(self) -> List[List[str]]:
        return self.board

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Helper method called by add_word()
        Expected behavior:
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word()
        (see documentation in boggle_game.py).
        If `word` is not present on the board, return None.
        """
        word = word.lower()
        #raise NotImplementedError("method find_word_in_board") # TODO: implement your code here
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        def dfs(board, word, i, j, pos, path, visited):
            if pos == len(word):
                return path
            if not (0 <= i < len(board) and 0 <= j < len(board[i])) or board[i][j] != word[pos] or visited[i][j]:
                return None
            visited[i][j] = True
            #print(f"Visiting ({i}, {j}), char: {word[pos]}, path: {path}")
            for di, dj in directions:
                next_path = dfs(board, word, i + di, j + dj, pos + 1, path + [(i, j)])
                if next_path:
                    return next_path
            visited[i][j] = False
            return None

        for row in range(self.size):
            for col in range(self.size):
                visited = [[False] * self.size for _ in range(self.size)]
                result = dfs(self.board, word, row, col, 0, [], visited)
                if result:
                    return result
        return None

    def add_word_test(self, word: str):
        word = word.lower()
        print(f"checking word: {word}")
        print("Board state in add_word_test: ")
        for row in self.board:
            print(row)
        
        location = self.find_word_in_board(word)
    
        print(f"Location found for '{word}' in add_word_test: {location}")
        return location

    def add_word(self, word: str) -> int:
        """This method is provided for you, but feel free to change it.
        """
        word = word.lower()
        print(f"checking word: {word}")
        print(self.find_word_in_board(word))
        #print(len(word) > SHORT)
        #print(word not in self.words)
        #print(game_dict.contains(word))
        #print((len(word) > SHORT and word not in self.words and game_dict.contains(word)))
        if (len(word) > SHORT and word not in self.words and game_dict.contains(word)):
            location = self.find_word_in_board(word)
            print(location is not None)
            if location is not None:
                self.last_added_word = location
                self.words.append(word)
                return len(word) - SHORT
        return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """This method is provided for you, but feel free to change it.
        """
        self.board = [[c.lower() for c in row] for row in board]

    def get_score(self) -> int:
        """This method is provided for you, but feel free to change it.
        """
        return sum([len(word) - SHORT for word in self.words])

    # def dictionary_driven_search(self) -> Set[str]:
    def dictionary_driven_search(self, dictionary) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """
        #raise NotImplementedError("method dictionary_driven_search") # TODO: implement your code here
        
        # found_words = set()
        # for word in self.dictionary:
        for word in dictionary:
            print(f"Checking word: {word}")
            #if self.find_word_in_board(word) and len(word) > SHORT:
                #found_words.add(word.lower())
            self.add_word(word)
        print(f"Found words are: {self.words}")
        return self.words
        

    def board_driven_search(self) -> Set[str]:
        """Find all words using a board-driven search.

        The board-driven search constructs a string using every path on
        the board and checks whether each string is a valid word in the
        dictionary.

        Returns:
            A set containing all words found on the board.
        """
        #raise NotImplementedError("method board_driven_search") # TODO: implement your code here
        def is_valid_word(word: str) -> bool:
            return len(word) > SHORT and self.dictionary.contains(word.lower())

        def is_valid_prefix(prefix: str) -> bool:
            return self.dictionary.is_prefix(prefix.lower())

        def search_path(i, j, path, visited, current_word):
            if is_valid_word(current_word):
                found_words.add(current_word.lower())
            visited.add((i,j))
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (0 <= ni < self.size and 0 <= nj < self.size and (ni, nj) not in visited):
                    new_word = current_word + self.board[ni][nj]
                    if is_valid_prefix(new_word):
                        search_path(ni, nj, path + [(ni, nj)], visited, new_word)
            visited.remove((i,j))

        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        found_words = set()
        for i in range(self.size):
            for j in range(self.size):
                search_path(i, j, [(i, j)], set(), self.board[i][j])
        return found_words

# handout
CUBE_FILE = "cubes.txt"
example_board = [
    ["E", "E", "C", "A"],
    ["A", "L", "E", "P"],
    ["H", "N", "B", "O"],
    ["Q", "T", "T", "Y"],
]
example_words = set("""
alec alee anele becap bent benthal blae blah blent bott cape capelan capo celeb cent
cento clan clean elan hale hant lane lean leant leap lent lento neap open pace peace
peel pele penal pent thae than thane toby toecap tope topee
""".upper().strip().split())
    
# call functions here
game = MyGameManager()
game.new_game(len(example_board), CUBE_FILE)
game.set_game(example_board)

print(f"find_word_in_board returns: {game.find_word_in_board("becap")}")
print(f"add_word returns: {game.add_word("becap")}")
print(f"add_word returns: {game.add_word_test("becap")}")
# print(game.dictionary_driven_search(example_words))
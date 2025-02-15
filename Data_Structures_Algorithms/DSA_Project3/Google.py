import typing
from typing import Optional, Dict, Set
from collections.abc import Iterator

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_word = False

class TrieDictionary():
    def __init__(self):
        self.root: TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()
                self._add_word_to_trie(word)

    def _add_word_to_trie(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def traverse(self, prefix: str) -> Optional[TrieNode]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def is_prefix(self, prefix: str) -> bool:
        return self.traverse(prefix) is not None

    def contains(self, word: str) -> bool:
        node = self.traverse(word)
        return node is not None and node.is_word

    def __iter__(self) -> typing.Iterator[str]:
        stack = [(self.root, "")]

        while stack:
            node, prefix = stack.pop()

            if node.is_word:
                yield prefix

            # Add child nodes to the stack
            for char, child_node in node.children.items():
                stack.append((child_node, prefix + char))

  
WORDS_FILE = "words.txt"
words: Set[str] = set()
with open(WORDS_FILE, "r") as fin:
    for line in fin:
        line = line.strip().upper()
        words.add(line)

def test_contains_all_example():
    #Test that the contains() returns True for all of the words specified in the dictionary file.

    # make dictionary
    #game_dict = trie_dictionary.TrieDictionary()
    game_dict = TrieDictionary()
    game_dict.load_dictionary(WORDS_FILE)

    for s in words:
        assert game_dict.contains(s)

test_contains_all_example
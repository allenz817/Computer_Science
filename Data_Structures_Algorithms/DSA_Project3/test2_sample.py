class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_word = False

class TrieDictionary:
    def __init__(self):
        self.root: TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        # Load words from a file and build the trie
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()
                node = self.root
                for char in word:
                    if char not in node.children:
                        node.children[char] = TrieNode()
                    node = node.children[char]
                node.is_word = True

    def contains(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

# Example usage
if __name__ == "__main__":
    WORDS_FILE = "test2_words.txt"
    test_word = "apple"

    game_dict = TrieDictionary()
    game_dict.load_dictionary(WORDS_FILE)

    if game_dict.contains(test_word):
        print(f"'{test_word}' exists in the dictionary.")
    else:
        print(f"'{test_word}' does not exist in the dictionary.")

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_word = False

class TrieDictionary:
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

    def print_trie(self, node: TrieNode = None, prefix: str = "") -> None:
        if node is None:
            node = self.root

        if node.is_word:
            print(prefix)

        for char, child in node.children.items():
            self.print_trie(child, prefix + char)

# Example usage:
if __name__ == "__main__":
    trie = TrieDictionary()
    trie.load_dictionary("words.txt")  # Replace with your actual dictionary file

    # Print the entire trie
    trie.print_trie()

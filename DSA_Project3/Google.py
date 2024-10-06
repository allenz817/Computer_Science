class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_word = False

class TrieDictionary(BoggleDictionary):
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

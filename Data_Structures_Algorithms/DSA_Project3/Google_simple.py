class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_word = False

root: TrieNode = TrieNode()

filename = "words.txt"
with open(filename) as wordsfile:
    for line in wordsfile:
        word = line.strip().lower()
        print(f"Processing word:{word}")

node = root
for char in word:
    if char not in node.children:
        node.children[char] = TrieNode()
    node = node.children[char]
node.is_word = True

def contains(word: str) -> bool:
    #node = self.traverse(word)
    #return (node is not None) and node.is_word
    node = root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    return node.is_word



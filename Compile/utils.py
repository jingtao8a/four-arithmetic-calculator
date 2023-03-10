class TireNode:
    def __init__(self):
        self.children = dict()
        self.is_end = False

class TireTree:
    def __init__(self, words):
        self.root = TireNode()
        for word in words:
            self.insert(word)

    def insert(self, word):
        node = self.root
        for i in word:
            if node.children.get(i) == None:
                node.children[i] = TireNode()
            node = node.children[i]
        node.is_end = True

    def find_common_prefixes(self):
        node = self.root
        prefix = ''
        while len(node.children.keys()) == 1 and node.is_end == False:
            ch = next(iter(node.children))
            prefix = prefix + ch
            node = node.children[ch]
        return prefix
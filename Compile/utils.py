class TireNode:
    def __init__(self):
        self.children = dict()
        self.is_end = False
        self.count = 1

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
            else:
                node = node.children[i]
                node.count += 1
        node.is_end = True

    def find_common_prefixes(self):
        common_prefixes = []
        for ch, node in self.root.children.items():
            if node.count > 1:
                prefix = ch
                parent_node_count = node.count
                while len(node.children) == 1 and list(node.children.values())[0].count == parent_node_count:
                    prefix += list(node.children.keys())[0]
                    node = list(node.children.values())[0]
                common_prefixes.append(prefix)
        return common_prefixes
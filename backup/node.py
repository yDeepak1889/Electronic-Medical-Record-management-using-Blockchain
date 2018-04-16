from utils import Util

BRANCH_NODE = 0
LINK_NODE = 1
DATA_NODE = 2

class Node:
    def __init__(self):
        self.hash = None
        self.type = None

    @property
    def get_hash(self):
        return self.hash

class BranchNode(Node):
    def __init__(self):
        super().__init__()
        self.children = [None] * 16
        self.type = BRANCH_NODE

    def calculate_hash(self):
        concated = ''
        for a_child in self.children:
            if a_child is not None:
                if a_child.get_hash is None:
                    a_child.calculate_hash()
                concated += a_child.get_hash
        self.hash = Util.get_hash(concated)

class LinkNode(Node):
    def __init__(self, block_number, addr, hash):
        super().__init__()
        self.blockNumber = block_number
        self.addr = addr
        self.hash = hash
        self.type = LINK_NODE

    def calculate_hash(self):
        ## got to that block, and then the address, and then use its 'calculate_hash' function
        pass


class DataNode(Node):
    def __init__(self):
        super().__init__()
        self.data = None
        self.type = DATA_NODE

    def calculate_hash(self):
        self.hash = Util.get_hash(self.data)

    def set_data(self, data):
        self.data = data

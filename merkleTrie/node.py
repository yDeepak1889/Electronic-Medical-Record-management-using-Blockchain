BRANCH_NODE = 0
LINK_NODE = 1
DATA_NODE = 2

class Node:
    def __init__(self):
        self.hash = None
        self.type = None

    @property
    def get_hash(self):
        return self.hash;

class BranchNode(Node):
    def __init__(self):
        super().__init__(self)
        self.children = [None] * 16
        self.type = BRANCH_NODE

    def calculate_hash(self):
        concated = ''
        for a_child in self.children:
            if a_child is not None:
                if a_child.get_hash() is None:
                    a_child.calculate_hash()
                concated += a_child.get_hash()
        self.hash = utils.get_hash_from_string(concated)


class LinkNode(Node):
    def __init__(self, block_number, addr):
        super().__init__(self)
        self.blockNumber = block_number
        self.addr = addr
        self.hash = calculate_hash(self)
        self.type = LINK_NODE

    def calculate_hash(self):
        ## got to that block, and then the address, and then use its 'calculate_hash' function
        pass


class DataNode(Node):
    def __init__(self):
        super().__init__(self)
        self.data = None
        self.type = DATA_NODE

    def calculate_hash(self):
        self.hash = self._get_hash(self._to_hex(self.data))

	def _to_hex(self, inp):
		str_inp = str(inp)
		str_inp = str_inp.encode('utf-8')
		return bytearray(str_inp).hex()

	def _get_hash(self, inp):
		inp = inp.enc

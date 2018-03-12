import hashlib

class node():
	"""node in a merkle tree"""
	def __init__(self):
		self.hash = None
		self.left = None
		self.right = None
		

class merkleKit():
	
	def __init__(self):
		self.leaf_nodes = []
		self.is_ready = False
		self.max_depth = 4
	
	def to_hex(self, inp):
		str_inp = str(inp)
		str_inp = str_inp.encode('utf-8')

		return bytearray(str_inp).hex()

	def get_hash(self, inp):
		inp = inp.encode('utf-8')
		return str(hashlib.sha256(inp).hexdigest())

	def add_node(self, inp):
		if(len(self.leaf_nodes) >= 2**(self.max_depth)):
			print('tree size exceeded, abort addition')
			return False
		
		self.is_ready = False
		hex_inp = self.to_hex(inp)
		hash_inp = self.get_hash(hex_inp)
		self.leaf_nodes.append(hash_inp)
		return hash_inp

	def create_tree(self):
		total = len(self.leaf_nodes)
		level = 0
		self.levels = []
		self.levels.append(self.leaf_nodes)
		level += 1
		while(total != 1):
			self.levels.append([])
			# self.levels[level].append([])

			for i in range(0, total, 2):
				if (i + 1 < total):
					concatenated_hash = self.levels[level - 1][i] + self.levels[level - 1][i]
					self.levels[level].append(self.get_hash(concatenated_hash))
				else:
					self.levels[level].append(self.levels[level - 1][i])
			
			total = len(self.levels[level])
			level += 1
		self.is_ready = False

	def _check_display_tree(self):
		for a_level in self.levels:
			for el in a_level:
				print(el, end="\t")
			print('\n*****\n')

mt = merkleKit()
mt.add_node('Aditya')
mt.add_node('Dewan')
mt.add_node('Again')
mt.create_tree()
mt._check_display_tree()
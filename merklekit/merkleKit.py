import hashlib
import pprint

# ******* Alternate approach, create nodes as this structure

# class node():
# 	"""node in a merkle tree"""
# 	def __init__(self):
# 		self.hash = None
# 		self.left = None
# 		self.right = None
		

class merkleKit():
	
	def __init__(self):
		self.leaf_nodes = []
		self.levels = []
		self.is_ready = False
		self.max_depth = 4

	def get_root_node(self):
		if(self.is_ready):
			return self.levels[len(self.levels) - 1][0]
		print('tree not ready yet, root node not assigned hash.')
		return False

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

	def get_proof(self, ind):
		if(ind >= len(self.leaf_nodes)):
			print ('index out of scope')
			return

		level = 0;
		proof = []
		total_current_level = len(self.levels[level])

		while(total_current_level >= 2):
			print(level, ind, total_current_level)
			if (ind % 2 == 0):
				pos = 'right'
				el_hash = None
				if ((ind + 1) < total_current_level):
					el_hash = self.levels[level][ind + 1]
				proof.append({el_hash: pos})
			else:
				pos = 'left'
				el_hash = self.levels[level][ind - 1]
				proof.append({el_hash: pos})
			
			level += 1
			ind = int(ind / 2)
			total_current_level = len(self.levels[level])

		return proof

	def check_proof(self, msg, proof):
		msg_hash = self.get_hash(msg)
		root_hash = self.get_root_node()

		for prf in proof:
			side_hash = list(prf.keys())[0]
				
			if(side_hash == None):
				continue
			
			side_dir = prf[side_hash]

			if (side_dir == 'left'):
				concatenated_hash = side_hash + msg_hash
				# replace msg_hash with thsi new one
				msg_hash = self.get_hash(concatenated_hash)
				print(concatenated_hash)
				print(msg_hash)
			else:
				concatenated_hash = msg_hash + side_hash
				# replace msg_hash with thsi new one
				msg_hash = self.get_hash(concatenated_hash)
				print(concatenated_hash)
				print(msg_hash)
		
		if (msg_hash == root_hash):
			return True
		else:
			return False

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
					# print(i, '-->', concatenated_hash)
					self.levels[level].append(self.get_hash(concatenated_hash))
				else:
					# print(i, '-->', self.levels[level - 1][i])
					self.levels[level].append(self.levels[level - 1][i])
			
			total = len(self.levels[level])
			level += 1
		self.is_ready = True

	def verify_proof():
		pass

	def _check_display_tree(self):
		for a_level in self.levels:
			for el in a_level:
				print(el, end="\t")
			print('\n*****\n')


mt = merkleKit()
mt.add_node('Aditya')
mt.add_node('Dewan')
mt.add_node('Again')
mt.add_node('1')
mt.add_node('2')
mt.add_node('3')
mt.add_node('4')
mt.add_node('5')
mt.add_node('6')
mt.add_node('7')
mt.add_node('8')
mt.add_node('9')
mt.add_node('10')
mt.add_node('11')
mt.add_node('12')
# mt.add_node('13')
# mt.add_node('14')
# mt.add_node('15')
mt.create_tree()
mt._check_display_tree()
print(0, mt.get_proof(0))
print(1, mt.get_proof(1))
print(14, mt.get_proof(14))
print(15, mt.get_proof(15))
print(16, mt.get_proof(16))
print('\ncheck proof\n')
print(mt.check_proof('Aditya', [{'045b61fa0ff73b2d265446228ea0dba753bfd652ca8a165737d604961f7d7ef8': 'right'}, {'70b6b35f0778664d7c5c1b697b54cddadbd49a77f83137a365de4c3d33eb113d': 'right'}, {'7a2901dd05a8421da242492c094b92578b435d6b76e9d7cacd2307ad60d24752': 'right'}, {'d9ae83f50466922a14955cc58a84771641c077b32eaa4de2bd5d83ee294a8fd8': 'right'}]))

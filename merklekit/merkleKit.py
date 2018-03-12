import hashlib

class merkleKit():
	
	def __init__(self):
		self.leaf_nodes = []
		self.is_ready = False
	
	def to_hex(self, inp):
		str_inp = str(inp)
		str_inp = str_inp.encode('utf-8')
		return hex(str_inp)

	def get_hash(self, inp):
		return str(hashlib.sha256(inp).hex_digest())
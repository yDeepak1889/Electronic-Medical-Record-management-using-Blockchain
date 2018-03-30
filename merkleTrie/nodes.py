import hashlib

class innerNode:
	def __init__(self):
		self.next = [None] * 16
		self.hash = None

class leafNode:
	def __init__(self):
		self.data = None
		self.hash = None

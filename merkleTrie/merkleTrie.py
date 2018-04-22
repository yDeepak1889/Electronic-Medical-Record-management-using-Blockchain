from merkleTrie.nodes import *
from merkleTrie.utils import Util
import json


class MerkleTrie:
	def __init__(self):
		self.root = None


	def updateHash (self, root = None):
		if not root:
			return

		nodeHash = ""
		for i in range(16):
			if root.next[i]:
				nodeHash = Util.get_hash(nodeHash + root.next[i].hash)
		root.hash = nodeHash
		return


	def traverseTrie (self, tranID, tranData, root = None):
		if not root:
			print("Error: root is None")
			return

		if len(tranID) == 1:
			indx = Util.getIndex(tranID[0])
			if root.next[indx]:
				print ('Invalid transaction ID : transaction ID already exists')
				return
			root.next[indx] = leafNode()
			root.next[indx].data = tranData
			root.next[indx].hash = Util.get_hash(json.dumps(tranData))
			self.updateHash (root)
			return

		indx = Util.getIndex(tranID[0])
		if not root.next[indx]:
			root.next[indx] = innerNode()

		self.traverseTrie(tranID[1:], tranData, root.next[indx])
		self.updateHash(root)
		return


	def updateForT (self, t, root = None):
		if root == None:
			return

		tranID = Util.get_hash(json.dumps(t))
		self.traverseTrie(tranID, t, root)


	def updateForAllTrans(self, trans):
		self.root = innerNode()

		for t in trans:
			self.updateForT(t, self.root)

		return self.root

	def getData (self, addr, root):
		if not root:
			return None
		if not addr:
			return root.data

		indx = Util.getIndex(addr[0])
		return self.getData(addr[1:], root.next[indx])

'''

trieRoot = MerkleTrie()

tran1 = {
	'to': Util.get_hash('abcdefgh1234')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': "This is a test amount1"
}


tran2 = {
	'to': Util.get_hash('abcdefgh12345')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': "This is a test amount2"
}
tran3 = {
	'to': Util.get_hash('abcdefgh12346')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': "This is a test amount3"
}
tran4 = {
	'to': Util.get_hash('abcdefgh12347')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': "This is a test amount4"
}
tran5 = {
	'to': Util.get_hash('abcdefgh12348')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': "This is a test amount5"
}

trans = [tran1, tran2, tran3, tran4, tran5]
root = trieRoot.updateForAllTrans (Util.sortItemBytransID(trans))

print(root.hash)
print (trieRoot.getData(tran3['to'], root))
'''

from nodes import *
from utils import *
import hashlib
import json

class StateTrie:
	def __init__(self):
		self.root = None


	def _populateWithPreviousNext (self, previousTrie = None, root = None):
		if previousTrie != None:
			for i in range(16):
				root.next[i] = previousTrie.next[i]
		return

	def updateHash (self, root = None):
		if not root:
			return 

		nodeHash = ""
		for i in range(16):
			if root.next[i]:
				nodeHash = Util.get_hash(nodeHash + root.next[i].hash)
		root.hash = nodeHash
		return


	def traverseTrie (self, addr, data, previousTrie = None, root = None):
		if len(addr) == 1:
			indx = Util.getIndex(addr[0])
			
			self._populateWithPreviousNext(previousTrie, root)
			
			root.next[indx] = leafNode()
			root.next[indx].data = data['data']
			root.next[indx].hash = Util.get_hash(json.dumps(data))
			
			self.updateHash (root)

			return

		self._populateWithPreviousNext(previousTrie, root)

		indx = Util.getIndex(addr[0])
		print ("New Node Created")
		root.next[indx] = innerNode()

		if not previousTrie:
			self.traverseTrie(addr[1:], data, previousTrie, root.next[indx])
		else:
			self.traverseTrie(addr[1:], data, previousTrie.next[indx], root.next[indx])

		self.updateHash (root)

		return


	def updateForT (self, t, previousTrie = None, root = None):
		if root == None:
			return

		toAddr = t['to']
		fromAddr = t['from']
		self.traverseTrie(toAddr, t, previousTrie, root)


	def updateForAllTrans(self, trans, previousTrie = None):
		self.root = innerNode()

		for t in trans:
			self.updateForT(t, previousTrie, self.root)

		return self.root


	def getData (self, addr, root):
		if not root:
			return None
		if not addr:
			return root.data

		indx = Util.getIndex(addr[0])
		return self.getData(addr[1:], root.next[indx])



trieRoot = StateTrie()

tran1 = {
	'to': Util.get_hash('abcdefgh1234')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data1"
}


tran2 = {
	'to': Util.get_hash('abcdefgh12345')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data2"
}
tran3 = {
	'to': Util.get_hash('abcdefgh12346')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data3"
}
tran4 = {
	'to': Util.get_hash('abcdefgh12347')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data4"
}
tran5 = {
	'to': Util.get_hash('abcdefgh12348')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data5"
}

trans = [tran1, tran2, tran3, tran4, tran5]
root = trieRoot.updateForAllTrans (trans)

print(root.hash)
print (trieRoot.getData(tran3['to'], root))



trieRoot1 = StateTrie()

tran11 = {
	'to': Util.get_hash('abcdefgh12341')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data11"
}
tran21 = {
	'to': Util.get_hash('abcdefgh12345')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data21"
}
tran31 = {
	'to': Util.get_hash('abcdefgh12346')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data31"
}
tran41 = {
	'to': Util.get_hash('abcdefgh12347')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data41"
}
tran51 = {
	'to': Util.get_hash('abcdefgh12348')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'data': "This is a test data51"
}

trans = [tran11]
root1 = trieRoot1.updateForAllTrans (trans, trieRoot.root)

print(root1.hash)

print (trieRoot1.getData(tran1['to'], root1))
print (trieRoot1.getData(tran2['to'], root1))
print (trieRoot1.getData(tran3['to'], root1))
print (trieRoot1.getData(tran4['to'], root1))
print (trieRoot1.getData(tran5['to'], root1))
print (trieRoot1.getData(tran11['to'], root1))
print (trieRoot1.getData(tran21['to'], root1))
print (trieRoot1.getData(tran31['to'], root1))
print (trieRoot.getData(tran41['to'], root1))
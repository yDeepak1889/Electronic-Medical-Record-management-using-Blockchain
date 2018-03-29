import hashlib
import json

def get_hash(inp):
		inp = inp.encode('utf-8')
		return str(hashlib.sha256(inp).hexdigest())

class innerNode:
	def __init__(self):
		self.next = [None] * 16
		self.hash = None

class leafNode:
	def __init__(self):
		self.data = {}
		self.hash = None


class StateTrie:
	def __init__(self):
		self.root = None
	

	def getIndex (self, ch) :
		if ord(ch) >= ord('a') and ord(ch) <= ord('f'):
			curPos = (ord(ch) - ord('a')) + 10
		else:
			curPos = ord(ch) - ord('0')

		return curPos


	def traverseTrie (self, addr, data, previousTrie = None, root = None):
		if len(addr) == 1:
			indx = self.getIndex(addr[0])
			
			if previousTrie != None:
				for i in range(16):
					root.next[i] = previousTrie.next[i]
			
			root.next[indx] = leafNode()
			root.next[indx].data = data['data']
			root.next[indx].hash = get_hash(json.dumps(data))
			nodeHash = ""
			for i in range(16):
				if root.next[i]:
					nodeHash = get_hash(nodeHash + root.next[i].hash)
			root.hash = nodeHash
			return

		if previousTrie != None:
			for i in range(16):
				root.next[i] = previousTrie.next[i]

		indx = self.getIndex(addr[0])
		print ("New Node Created")
		root.next[indx] = innerNode()

		if not previousTrie:
			self.traverseTrie(addr[1:], data, previousTrie, root.next[indx])
		else:
			self.traverseTrie(addr[1:], data, previousTrie.next[indx], root.next[indx])

		nodeHash = ""
		for i in range(16):
			if root.next[i]:
				nodeHash = get_hash(nodeHash + root.next[i].hash)

		root.hash = nodeHash


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

		indx = self.getIndex(addr[0])
		return self.getData(addr[1:], root.next[indx])

trieRoot = StateTrie()
tran1 = {
	'to': get_hash('abcdefgh1234')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data1"
}


tran2 = {
	'to': get_hash('abcdefgh12345')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data2"
}
tran3 = {
	'to': get_hash('abcdefgh12346')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data3"
}
tran4 = {
	'to': get_hash('abcdefgh12347')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data4"
}
tran5 = {
	'to': get_hash('abcdefgh12348')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data5"
}

trans = [tran1, tran2, tran3, tran4, tran5]

root = trieRoot.updateForAllTrans (trans)

print(root.hash)

print (trieRoot.getData(tran3['to'], root))



trieRoot1 = StateTrie()
tran11 = {
	'to': get_hash('abcdefgh12341')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data11"
}


tran21 = {
	'to': get_hash('abcdefgh12345')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data21"
}
tran31 = {
	'to': get_hash('abcdefgh12346')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data31"
}
tran41 = {
	'to': get_hash('abcdefgh12347')[:20],
	'from': get_hash('abcdefgh1234')[:20],
	'data': "This is a test data41"
}
tran51 = {
	'to': get_hash('abcdefgh12348')[:20],
	'from': get_hash('abcdefgh1234')[:20],
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

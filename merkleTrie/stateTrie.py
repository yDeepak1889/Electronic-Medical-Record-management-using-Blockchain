from merkleTrie.nodes import *
from merkleTrie.utils import *
import hashlib
import json

class StateTrie:
	

	@staticmethod
	def _populateWithPreviousNext (previousTrie = None, root = None):
		if previousTrie != None:
			for i in range(16):
				root.next[i] = previousTrie.next[i]
		return


	@staticmethod
	def updateHash (root = None):
		if not root:
			return 

		nodeHash = ""
		for i in range(16):
			if root.next[i]:
				nodeHash = Util.get_hash(nodeHash + root.next[i].hash)
		root.hash = nodeHash
		return


	@staticmethod
	def traverseTrie (addr, amount, multiplier = 1, previousTrie = None, root = None):
		if len(addr) == 1:
			indx = Util.getIndex(addr[0])
			
			StateTrie._populateWithPreviousNext(previousTrie, root)
			
			curBal = 0
			
			if root.next[indx]:
				curBal = root.next[indx].data
				#print (curBal, '----')

			root.next[indx] = leafNode()
			root.next[indx].data = curBal + multiplier*amount
			#print(root.next[indx].data)
			root.next[indx].hash = Util.get_hash(json.dumps(amount))
			
			StateTrie.updateHash (root)

			return

		StateTrie._populateWithPreviousNext(previousTrie, root)

		indx = Util.getIndex(addr[0])
		#print ("New Node Created")
		root.next[indx] = innerNode()

		if not previousTrie:
			StateTrie.traverseTrie(addr[1:], amount, multiplier, previousTrie, root.next[indx])
		else:
			StateTrie.traverseTrie(addr[1:], amount, multiplier, previousTrie.next[indx], root.next[indx])

		StateTrie.updateHash (root)

		return


	@staticmethod
	def updateForT (t, previousTrie = None):
		toAddr = t['to']
		fromAddr = t['from']
		root = innerNode()
		StateTrie.traverseTrie(toAddr, t['amount'], 1, previousTrie, root)
		previousTrie = root
		root = innerNode()
		StateTrie.traverseTrie(fromAddr, t['amount'], -1, previousTrie, root)
		return root

	
	@staticmethod
	def updateForAllTrans(trans, previousTrie = None):
		#print(trans)
		root = None
		for t in trans:
			root = updateForT(t, previousTrie)
			previousTrie = root

		return root

	@staticmethod
	def getData (addr, root):
		if not root:
			return None
		if not addr:
			#print(root.data)
			return root.data

		indx = Util.getIndex(addr[0])
		return StateTrie.getData(addr[1:], root.next[indx])


'''
trieRoot = StateTrie()

tran1 = {
	'to': Util.get_hash('abcdefgh1234')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1
	}


tran2 = {
	'to': Util.get_hash('abcdefgh12345')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1
	}
tran3 = {
	'to': Util.get_hash('abcdefgh12346')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1
	}
tran4 = {
	'to': Util.get_hash('abcdefgh12347')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1
	}
tran5 = {
	'to': Util.get_hash('abcdefgh12348')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1
	}

trans = [tran1, tran2, tran3, tran4, tran5]
root = trieRoot.updateForAllTrans (trans)

print(root.hash)
print (trieRoot.getData(tran1['to'], root))



trieRoot1 = StateTrie()

tran11 = {
	'to': Util.get_hash('abcdefgh12341')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1

}
tran21 = {
	'to': Util.get_hash('abcdefgh12345')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1

}
tran31 = {
	'to': Util.get_hash('abcdefgh12346')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1

}
tran41 = {
	'to': Util.get_hash('abcdefgh1234711')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': 1

}
tran51 = {
	'to': Util.get_hash('abcdefgh12348')[:20],
	'from': Util.get_hash('abcdefgh1234')[:20],
	'amount': "This is a test amount51"
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
print (trieRoot1.getData(tran41['to'], root1))
'''
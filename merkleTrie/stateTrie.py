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
	def traverseTrie (addr, tran, previousTrie = None, root = None, isHos = False):
		if len(addr) == 1:
			indx = Util.getIndex(addr[0])

			StateTrie._populateWithPreviousNext(previousTrie, root)

			curData = None

			if root.next[indx]:
				curData = root.next[indx].data

			root.next[indx] = leafNode()
			root.next[indx].data = curData

			#Hospital sends record of a patient
			type_ = tran['type']
			#print(type_, isHos)

			if type_ == 0 and isHos == False:
				dataToUpdate = {
				tran['info']['diseaseId']: {
						"docs": [{"link":tran['info']['docLink'], "hash":tran['info']['hash']}],
						"permmissions": [tran['info']['permmissions']]
					}
				}

				if root.next[indx].data:
					if tran['from'] in root.next[indx].data:
						if tran['info']['diseaseId'] in root.next[indx].data[tran['from']]:
							print (root.next[indx].data[tran['from']])
							root.next[indx].data[tran['from']][tran['info']['diseaseId']]["docs"].append({"link":tran['info']['docLink'], "hash":tran['info']['hash']})
							root.next[indx].data[tran['from']][tran['info']['diseaseId']]["permmissions"].append(tran['info']['permmissions'])
						else:
							root.next[indx].data[tran['from']] = dataToUpdate
					else:
						root.next[indx].data[tran['from']] = dataToUpdate

				else:
					root.next[indx].data = {
						tran['from']: dataToUpdate
					}
			#Patient grants permmission to new hospital to access data of specified hospitalId and diseadeId
			elif type_ == 1:
				root.next[indx].data[tran['info']['hospitalId']][tran['info']['diseaseId']]['permmissions'].append(tran['to'])

			elif type_ == 2:
				if tran['to'] in root.next[indx].data[tran['info']['hospitalId']][tran['info']['diseaseId']]['permmissions']:
					root.next[indx].data[tran['info']['hospitalId']][tran['info']['diseaseId']]['permmissions'].remove(tran['to'])


			elif type_ == 0 and isHos == True:
				dataToUpdate = {
					tran['info']['diseaseId']: [tran['info']['hash']]
				}

				if root.next[indx].data:
					if tran['to'] in root.next[indx].data:
						if tran['info']['diseaseId'] in root.next[indx].data[tran['to']]:
							root.next[indx].data[tran['to']][tran['info']['diseaseId']].append(tran['info']['hash'])
						else:
							root.next[indx].data[tran['to']][tran['info']['diseaseId']] = [tran['info']['hash']]
					else:
						root.next[indx].data[tran['to']] = dataToUpdate
				else:
					root.next[indx].data = {
						tran['to']: dataToUpdate
					}
				#print (dataToUpdate)

			root.next[indx].hash = Util.get_hash(json.dumps(root.next[indx].data))

			#print (root.next[indx].data)

			StateTrie.updateHash (root)

			return

		StateTrie._populateWithPreviousNext(previousTrie, root)

		indx = Util.getIndex(addr[0])

		root.next[indx] = innerNode()

		if not previousTrie:
			StateTrie.traverseTrie(addr[1:], tran, previousTrie, root.next[indx], isHos)
		else:
			StateTrie.traverseTrie(addr[1:], tran, previousTrie.next[indx], root.next[indx], isHos)

		StateTrie.updateHash (root)

		return


	@staticmethod
	def updateForT (t, previousTrie = None, isHos=False):
		#print (isHos)
		if isHos:
			toAddr = t['from']
		elif t['type'] != 0:
			toAddr = t['from']
			fromAddr = t['to']
		else:
			toAddr = t['to']
			fromAddr = t['from']

		root = innerNode()

		StateTrie.traverseTrie(toAddr, t, previousTrie, root, isHos)
		return root


	@staticmethod
	def updateForAllTrans(trans, previousTrie = None, isHos=False):
		#print (isHos)
		root = previousTrie
		for t in trans:
			if isHos:
				if t['type'] == 0:
					#print (t['type'], t)
					root = StateTrie.updateForT(t, previousTrie, isHos)
					previousTrie = root
			else:
				root = StateTrie.updateForT(t, previousTrie, isHos)
				previousTrie = root

		return root

	@staticmethod
	def getData (addr, root):
		#print (addr, root)
		if not root:
			return None
		if not addr:
			return root.data

		indx = Util.getIndex(addr[0])
		return StateTrie.getData(addr[1:], root.next[indx])



#For Testing Purpose
'''
trieRoot = StateTrie()

diseaseId = "abcdefgh1234"
docLink = "http://www.dummy.com"
from_ = Blockchain.hash('abcdefgh1234')[:20]

tran1 = {
	'from': Util.get_hash('abcdefgh123477')[:20],
	'to': Util.get_hash('abcdefgh12345')[:20],
	'type' : 0,
	'info':{
		'diseaseId' : diseaseId,
		'docLink': docLink,
		'permmissions' : [from_]
		}
	}


# tran2 = {
# 	'from': Util.get_hash('abcdefgh12345')[:20],
# 	'to': Util.get_hash('abcdefgh1234')[:20],
# 	'type' : 0,
# 	'info':{
# 		'diseaseId' : diseaseId,
# 		'docLink': docLink,
# 		'permmissions' : [from_]
# 		}
# 	}
# tran3 = {
# 	'from': Util.get_hash('abcdefgh12346')[:20],
# 	'to': Util.get_hash('abcdefgh1234')[:20],
# 	'type' : 0,
# 	'info':{
# 		'diseaseId' : diseaseId,
# 		'docLink': docLink,
# 		'permmissions' : [from_]
# 		}
# 	}
# tran4 = {
# 	'from': Util.get_hash('abcdefgh12347')[:20],
# 	'to': Util.get_hash('abcdefgh1234')[:20],
# 	'type' : 0,
# 	'info':{
# 		'diseaseId' : diseaseId,
# 		'docLink': docLink,
# 		'permmissions' : [from_]
# 		}
# 	}
# tran5 = {
# 	'from': Util.get_hash('abcdefgh12348')[:20],
# 	'to': Util.get_hash('abcdefgh1234')[:20],
# 	'type' : 0,
# 	'info':{
# 		'diseaseId' : diseaseId,
# 		'docLink': docLink,
# 		'permmissions' : [from_]
# 		}
# 	}

trans = [tran1]
root = trieRoot.updateForAllTrans (trans)

#print(root.hash)
#print (trieRoot.getData(tran1['to'], root))



trieRoot1 = StateTrie()

diseaseId = "abcdefgh1234"
docLink = "http://www.dummy.comm"
from_ = Util.get_hash('abcdefgh123')[:20]

tran11 = {
	'from': Util.get_hash('abcdefgh1234')[:20],
	'to': Util.get_hash('abcdefgh12345')[:20],
	'type' : 0,
	'info':{
		'diseaseId' : diseaseId,
		'docLink': docLink,
		'permmissions' : [from_]
		}
	}


tran21 = {
	'from': Util.get_hash('abcdefgh12345')[:20],
	'to': Util.get_hash('abcdefgh1234')[:20],
	'type' : 0,
	'info':{
		'diseaseId' : diseaseId,
		'docLink': docLink,
		'permmissions' : [from_]
		}
	}
tran31 = {
	'from': Util.get_hash('abcdefgh12346')[:20],
	'to': Util.get_hash('abcdefgh1234')[:20],
	'type' : 0,
	'info':{
		'diseaseId' : diseaseId,
		'docLink': docLink,
		'permmissions' : [from_]
		}
	}
tran41 = {
	'from': Util.get_hash('abcdefgh12347')[:20],
	'to': Util.get_hash('abcdefgh1234')[:20],
	'type' : 0,
	'info':{
		'diseaseId' : diseaseId,
		'docLink': docLink,
		'permmissions' : [from_]
		}
	}
tran51 = {
	'from': Util.get_hash('abcdefgh12348')[:20],
	'to': Util.get_hash('abcdefgh1234')[:20],
	'type' : 0,
	'info':{
		'diseaseId' : diseaseId,
		'docLink': docLink,
		'permmissions' : [from_]
		}
	}

trans = [tran11]
root1 = trieRoot1.updateForAllTrans (trans, root)

#print(root1.hash)

# print (trieRoot1.getData(tran1['to'], root1))
# print (trieRoot1.getData(tran2['to'], root1))
# print (trieRoot1.getData(tran3['to'], root1))
# print (trieRoot1.getData(tran4['to'], root1))
# print (trieRoot1.getData(tran5['to'], root1))
#print (trieRoot1.getData(tran11['to'], root1))
# print (trieRoot1.getData(tran21['to'], root1))
# print (trieRoot1.getData(tran31['to'], root1))
# print (trieRoot1.getData(tran41['to'], root1))
'''

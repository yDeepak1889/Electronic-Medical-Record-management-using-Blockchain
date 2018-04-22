import requests
from urllib.parse import urlparse
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import json
import hashlib
from merkleTrie.stateTrie import *
from merkleTrie.merkleTrie import *
from merkleTrie.utils import *


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.currentTransaction = []
        self.newBlock(100, 0)
        self.nodes = set()

    def registerNode (self, address):
        parsedURL = urlparse(address)

        if parsedURL.netloc:
            self.nodes.add(parsedURL.netloc)
        elif parsedURL.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsedURL.path)
        else:
            raise ValueError('Invalid URL')

    def newBlock(self, proof, previousHash=None):

        if len(self.currentTransaction) == 0 and len(self.chain) > 0:
            #rint (len(self.chain))
            #print ('Booom')
            return None

        merkleTrie = MerkleTrie()
        merkleRoot = merkleTrie.updateForAllTrans (self.currentTransaction)


        if len(self.chain) == 0:
            preH = previousHash
            stateTrieRoot = StateTrie.updateForAllTrans (self.currentTransaction)
        else:
            preH = self.hash(self.chain[-1][0])
            stateTrieRoot = StateTrie.updateForAllTrans (self.currentTransaction, self.chain[-1][1]['stateTrieRoot'])

        if not stateTrieRoot:
            stateHash = None
        else:
            stateHash = stateTrieRoot.hash

        if not merkleRoot:
            merkleHash = None
        else:
            merkleHash = merkleRoot.hash

        block = [
            {'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.currentTransaction,
            'proof': proof,
            'previousHash': preH,
            'stateTrieHash': stateHash,
            'merkleRootHash': merkleHash
            },
            {
            'stateTrieRoot': stateTrieRoot,
            'merkleTrieRoot': merkleRoot
            }
        ]
        block[0]['hash'] = Blockchain.hash(block[0])

        self.currentTransaction = []
        self.chain.append(block)
        return block

    def newTransaction(self, sender, recipient, type_, info):
        self.currentTransaction.append({
            'from': sender,
            'to': recipient,
            'type': type_,
            'info': info
        })
        #print (info)
        return self.lastBlock[0]['index'] + 1

    @staticmethod
    def hash(block):
        blockString = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()

    @property
    def lastBlock(self):
        return self.chain[-1]

    def proofOfWork(self, lastProof):
        proof = 0
        while self.validProof(lastProof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def validProof(lastProof, proof):
        guess = str(str(lastProof) + str(proof)).encode()
        guessHash = hashlib.sha256(guess).hexdigest()
        return guessHash[:4] == "0000"

    def validChain (self, chain):
        lastBlock = chain[0][0]
        currentIndex = 1

        while currentIndex < len(chain):
            block = chain[currentIndex][0]

            if block['previousHash'] != self.hash(lastBlock):
                return False

            lastBlock = block
            currentIndex += 1

        return True

    def resolveConflicts(self):
        neighours = self.nodes
        newChain = None

        maxLength = len(self.chain)

        for node in neighours:
            response = requests.get('http://' + node + '/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

            if length > maxLength and self.validChain(chain):
                maxLength = length
                newChain = chain

        if newChain:
            print ("New Chain found")
            self.chain = newChain
            length = len(chain)
            for i in range(1, length):
                StateTrie.updateForAllTrans(self.chain[i][0]['transactions'], self.chain[i-1][1]['stateTrieRoot'])
            return True

        return False

    def submitRecordTransaction(self, from_, to_, diseaseId, docLink, hash_):
        hashOfDoc = Util.get_hash(docLink) #update this to get hash of original doc
        type_ = 0
        info = {
            'diseaseId' : diseaseId,
            'docLink': docLink,
            'permmissions' : from_,
            'hash': hash_
        }
        return self.newTransaction(from_, to_, type_, info)

    def grantRevokeAccessTransaction(self, from_, to_, hospitalId, diseaseId, type_=1):
        lastBlk = self.lastBlock
        stateTrie = lastBlk[1]['stateTrieRoot']

        dataBlock = StateTrie.getData(from_, stateTrie)
        #print (dataBlock)
        if not dataBlock:
            return False

        if hospitalId in dataBlock:
            if not diseaseId in dataBlock[hospitalId]:
                return False
        else:
            return False

        info = {
            'hospitalId' : hospitalId,
            'diseaseId': diseaseId
        }

        #print (info)
        return self.newTransaction(from_, to_, type_, info)


    def getPatientData(self, addr):
        lastBlk = self.lastBlock
        stateTrie = lastBlk[1]['stateTrieRoot']

        dataBlock = StateTrie.getData(addr, stateTrie)
        
        if not dataBlock:
            return {'No Record Exists'}

        return dataBlock


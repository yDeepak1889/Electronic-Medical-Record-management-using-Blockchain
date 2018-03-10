import requests
from urllib.parse import urlparse
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import json
import hashlib


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
        if len(self.chain) == 0:
            preH = previousHash
        else:
            preH = self.hash(self.chain[-1])

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.currentTransaction,
            'proof': proof,
            'previousHash': preH
        }

        self.currentTransaction = []
        self.chain.append(block)
        return block

    def newTransaction(self, sender, recipient, amount):
        self.currentTransaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.lastBlock['index'] + 1

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
        lastBlock = chain[0]
        currentIndex = 1

        while currentIndex < len(chain):
            block = chain[currentIndex]

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
            self.chain = newChain
            return True

        return False


app = Flask(__name__)
nodeIdentifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.lastBlock
    lastProof = last_block['proof']
    proof = blockchain.proofOfWork(lastProof)

    blockchain.newTransaction(
        sender="0",
        recipient=nodeIdentifier,
        amount=1

    )

    previousHash = blockchain.hash(last_block)
    block = blockchain.newBlock(proof, previousHash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transaction': block['transactions'],
        'proof': block['proof'],
        'previousHash': previousHash
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def newTransaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return "Missing values", 400

    index = blockchain.newTransaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': str('Transaction will be added to Block ' + str(index))}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def fullChain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def registerNodes():
    values = request.get_json()

    nodes = values.get('nodes')
    print(nodes)
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.registerNode(node)

    response = {
        'message': 'New nodes have been added',
        'length': len(blockchain.nodes),
        'total_nodes': list(blockchain.nodes)
    }

    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolveConflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }

    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

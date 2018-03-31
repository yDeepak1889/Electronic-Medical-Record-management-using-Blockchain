from blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4
from merkleTrie.stateTrie import StateTrie

app = Flask(__name__)
nodeIdentifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.lastBlock
    lastProof = last_block[0]['proof']
    proof = blockchain.proofOfWork(lastProof)
    previousHash = blockchain.hash(last_block[0])
    block = blockchain.newBlock(proof, previousHash)

    if block:
        response = {
            'message': "New Block Forged",
            'index': block[0]['index'],
            'transaction': block[0]['transactions'],
            'proof': block[0]['proof'],
            'previousHash': previousHash
        }
    else :
        response = {
            'message' : 'Empty transaction pool'
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

    fullChainArr = []
    for block in blockchain.chain:
        fullChainArr.append(block[0])

    response = {
        'chain': fullChainArr,
        'length': len(fullChainArr)
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
            'message': 'Your chain was replaced',
            'new_chain': blockchain.chain
        }

    else:
        response = {
            'message': 'Your chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


@app.route('/getBalance', methods=['POST'])
def getBalance():
    values = request.get_json()
    addr = values.get('addr')
    response = {
        'balance': None
    }
    if len(blockchain.chain) < 2:
        return jsonify(response), 201

    #print(addr)
    latestStateTrie = blockchain.lastBlock[1]['stateTrieRoot']
    #print(latestStateTrie)
    response['balance'] = StateTrie.getData(addr, latestStateTrie)
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

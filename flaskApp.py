from blockchain import Blockchain

app = Flask(__name__)
nodeIdentifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = Blockchain.lastBlock
    lastProof = last_block['proof']
    proof = Blockchain.proofOfWork(lastProof)

    Blockchain.newTransaction(
        sender="0",
        recipient=nodeIdentifier,
        amount=1

    )

    previousHash = Blockchain.hash(last_block)
    block = Blockchain.newBlock(proof, previousHash)

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

    index = Blockchain.newTransaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': str('Transaction will be added to Block ' + str(index))}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def fullChain():
    response = {
        'chain': Blockchain.chain,
        'length': len(Blockchain.chain)
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
        Blockchain.registerNode(node)

    response = {
        'message': 'New nodes have been added',
        'length': len(Blockchain.nodes),
        'total_nodes': list(Blockchain.nodes)
    }

    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = Blockchain.resolveConflicts()

    if replaced:
        response = {
            'message': 'Your chain was replaced',
            'new_chain': Blockchain.chain
        }

    else:
        response = {
            'message': 'Your chain is authoritative',
            'chain': Blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

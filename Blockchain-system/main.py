from flask import Flask, request, Response, jsonify
from json import dumps
from flask_restful import Api
from Blockchain import BlockChain
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
import json
from uuid import uuid4

app = Flask(__name__)
api = Api(app)
blockchain = BlockChain()
node_identifier = str(uuid4()).replace('-', '')

@app.route('/import', methods=['POST'])
def insertTransaction():
    try:
        data = request.json.get('data')
        for i in data:
            sender = i.get('sender')
            recipient = i.get('recipient')
            amount = i.get('amount')
            blockchain.new_transaction(sender, recipient, amount)
        return json.dumps(data) + ' added to Block with index ' + str(len(blockchain.chain) + 1), 200
    except:
        return 400

@app.route('/getBlock/<index>', methods=['GET'])
def getBlock(index):
    if int(index) > len(blockchain.chain):
        return 'Index out of range', 404
    elif int(index) <= 0:
        return 'Wrong index', 404
    else:
        return json.dumps(blockchain.chain[int(index) - 1].block_info()), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = []
    length = len(blockchain.chain)
    data = [i.block_info() for i in blockchain.chain]
    response.append({'length':length, 'data': data})
    return json.dumps(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.chain[-1]
    last_proof = last_block.block_info().get('proof')
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.chain[-1].compute_hash
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block.block_info().get('index'),
        'data': block.block_info().get('data'),
        'proof': block.block_info().get('proof'),
        'prevHash': block.block_info().get('prevHash'),
    }
    return jsonify(response), 200

@app.route('/node/register', methods=['POST'])
def register():
    nodes = request.json.get('node')
        
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

def run_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=blockchain.new_block, trigger="interval", seconds=3)
    scheduler.start()
    return 'Scheduled several long running tasks.', 200

run_tasks()
app.run()
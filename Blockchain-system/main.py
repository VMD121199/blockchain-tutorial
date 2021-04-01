from flask import Flask, request, Response, jsonify
from json import dumps
from flask_restful import Resource, Api
from Blockchain import BlockChain
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
import json

app = Flask(__name__)
api = Api(app)
blockchain = BlockChain()

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

def run_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=blockchain.new_block, trigger="interval", seconds=3)
    scheduler.start()
    return 'Scheduled several long running tasks.', 200

run_tasks()
app.run()
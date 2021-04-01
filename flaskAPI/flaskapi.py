from flask import Flask, request, Response
from json import dumps
from flask_restful import Resource, Api
from Blockchain import BlockChain
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
import json

app = Flask(__name__)
api = Api(app)
blockchain = BlockChain()

@app.route('/hello') # Routes you to the page with http://127.0.0.1:5000/hello/
def hello():
    return 'Hello, World'

@app.route('/import', methods=['POST'])
def insertTransaction():
    data = request.json.get('data')
    for i in data:
        sender = i.get('sender')
        recipient = i.get('recipient')
        amount = i.get('amount')
        blockchain.new_transaction(sender, recipient, amount)
    return 'OK'

# @app.route('/getBlock', methods=['GET'])
# def getBlock(index):

def run_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=blockchain.new_block, trigger="interval", seconds=3)
    scheduler.start()
    return 'Scheduled several long running tasks.', 200

run_tasks()
app.run()
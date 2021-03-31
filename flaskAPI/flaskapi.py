from flask import Flask, request, Response
from json import dumps
from flask_restful import Resource, Api
from Blockchain import BlockChain
import schedule
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
api = Api(app)

@app.route('/hello') # Routes you to the page with http://127.0.0.1:5000/hello/
def hello():
    return 'Hello, World'

@app.route('/import', methods=['POST'])
def insertTransaction():
    content = request.json
    return content

@app.route('/start', methods=['POST'])
def run_tasks():
    app.apscheduler.add_job(func=create_block, trigger='date', args=[i], id='j'+str(i))
 
    return 'Scheduled several long running tasks.', 200

def create_block():
    blockchain = BlockChain()
    schedule.every(5).seconds.do(blockchain.new_block)
    while True:
        schedule.run_pending

app.run()
from flask import Flask, request
from json import dumps
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/hello') # Routes you to the page with http://127.0.0.1:5000/hello/
def hello():
    return 'Hello, World'

@app.route('/import', methods=['POST'])
def insertTransaction():
    content = request.json
    print(content)
    return response

app.run()
import hashlib
import json
from time import time
import random
# Block
class Block:
    def __init__(self, index, timestamp, data, prevHash, nonce):
        '''
            Default constructor for creating a block.
            Parameters
            ----------
            index : int
                The index of the block
            timestamp: long
                Timestamp in epoch, number of seconds since 1 Jan 1970
            data : object
                The actual data that needs to be stored on block chain
            prevHash : str
                The hash of the previous block
            nonce : str
                The nonce which has been mined
            target: int
                Number of leading zeros
        '''
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prevHash = prevHash
        self.nonce = nonce
        super().__init__()

    def block_info(self):
        return {'index': self.index, 'timestamp': self.timestamp, 'data': self.data, 'prevHash': self.prevHash, 'nonce': self.nonce, 'currHash': self.compute_hash()}

    def compute_hash(self):
        '''
            Compute sha1 hash and convert it into hexadecimal string, json.dumps
            uses ":" separator without space
            Returns
            -------
            str
                sha1 hash of the attributes converted into hexadecimal string
        '''
        # currHash = sha1(index+timestamp+data+prevHash+nonce)
        return hashlib.sha256(json.dumps(self.__dict__, separators=(',', ':')) \
        .encode("utf-8")).hexdigest()

# Blockchain
class BlockChain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block("000000000000000000000000000000")
    
    @property
    def last_block(self):
        #return Block with index
        return self.chain[-1]

    def new_block(self, previousHash=None):
        block = Block(index = len(self.chain)+1,
                            timestamp = time(),
                            data = self.pending_transactions,
                            prevHash = previousHash if len(self.chain) == 0 else Block.compute_hash(self.chain[len(self.chain) - 1]),
                            nonce = random.randint(0, 1514528022))
        self.pending_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        # Error: fix by get block by index
        return self.last_block[len(self.chain)] + 1

if __name__ == "__main__":
    blockchain = BlockChain()
    t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
    t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
    t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
    blockchain.new_block()
    t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
    t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
    t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
    for i in blockchain.chain:
        print("------------------------INFO----------------------------")
        print(i.block_info())
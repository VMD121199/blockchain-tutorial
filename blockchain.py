import hashlib
import json
from time import time
import random
from Block import Block
import schedule

# Blockchain
class BlockChain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block("000000000000000000000000000000")
    
    def new_block(self, previousHash=None):
        block = Block(index = len(self.chain)+1,
                            timestamp = time(),
                            data = self.pending_transactions,   
                            prevHash = previousHash if len(self.chain) == 0 else Block.compute_hash(self.chain[len(self.chain) - 1]),
                            nonce = random.randint(0, 1514528022))
        self.pending_transactions = []
        self.chain.append(block)
        print(block.block_info())
        return block

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.chain[-1]


if __name__ == "__main__":
    blockchain = BlockChain()
    schedule.every(5).seconds.do(blockchain.new_block)
    while True:
        schedule.run_pending()
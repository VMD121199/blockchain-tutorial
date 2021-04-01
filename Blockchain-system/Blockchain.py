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
        self.new_block(1000, "00000000000000000000000000000000000000000000000000000")
    
    def new_block(self, Proof=None, previousHash=None):
        block = Block(index = len(self.chain)+1,
                            timestamp = time(),
                            data = self.pending_transactions,   
                            prevHash = previousHash if len(self.chain) == 0 else Block.compute_hash(self.chain[len(self.chain) - 1]),
                            nonce = random.randint(0, 2**32),
                            proof = Proof if len(self.chain) == 0 else self.proof_of_work(self.chain[-1].proof))
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
    
    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
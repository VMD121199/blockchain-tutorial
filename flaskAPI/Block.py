import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, data, prevHash, nonce, proof):
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
        self.proof = proof
        self.target = None
        super().__init__

    def getitem(self, index):
        return self.data[index]

    def block_info(self):
        return {'index': self.index, 'timestamp': self.timestamp, 'data': self.data, 'prevHash': self.prevHash, 'nonce': self.nonce, 'currHash': self.compute_hash(), 'proof': self.proof}

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
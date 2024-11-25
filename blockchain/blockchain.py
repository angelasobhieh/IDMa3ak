import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, authority, next_hash=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.authority = authority  # For Proof of Authority
        self.next_hash = next_hash

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self, authority):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.authority = authority  # Authority node for PoA

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0", self.authority)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine(self):
        if not self.pending_transactions:
            return None
        
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=latest_block.hash,
            authority=self.authority
        )
        # Link blocks forward
        latest_block.next_hash = new_block.hash
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

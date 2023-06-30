import hashlib
import json
import datetime
import numpy as np

# Define the blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(0, 'genesis_hash')
        self.difficulty = 4

    # Create a block and add to the chain
    def create_block(self, nonce, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.transactions,
            'nonce': nonce,
            'previous_hash': previous_hash,
        }
        self.transactions = []
        self.chain.append(block)
        return block

    # Get the previous block
    def previous_block(self):
        return self.chain[-1]

    # Proof of work algorithm
    def proof_of_work(self):
        previous_hash = self.hash_block(self.previous_block())
        nonce = 0
        while self.valid_proof(self.transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    # Check if the proof is valid
    def valid_proof(self, transactions, previous_hash, nonce):
        guess = (str(transactions) + str(previous_hash) + str(nonce)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == '0' * self.difficulty

    # Hash a block
    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # Add a transaction to the block
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    # Check if the chain is valid
    """def valid_chain(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block['previous_hash'] != self.hash_block(previous_block):
                return False
            transactions = block['transactions'][:-1]
            transaction_elements = ['sender', 'receiver', 'amount']
            expected_hash = block['transactions'][-1]['hash']
            for transaction in transactions:
                if set(transaction.keys()) != set(transaction_elements):
                    return False
                transaction_hash = self.hash_transaction(transaction)
                if transaction_hash != transaction['hash']:
                    return False
                expected_hash = hashlib.sha256((expected_hash + transaction_hash).encode()).hexdigest()
            if expected_hash != block['previous_hash']:
                return False
            previous_block = block
            block_index += 1
        return True
"""

    # Check if the chain is valid
    def valid_chain(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block['previous_hash'] != self.hash_block(previous_block):
                return False
            transactions = block['transactions'][:-1]
            transaction_elements = ['sender', 'receiver', 'amount']
            expected_hash = block['transactions'][-1]['hash']
            for transaction in transactions:
                if set(transaction.keys()) != set(transaction_elements):
                    return False
                transaction_hash = self.hash_transaction(transaction)
                if transaction_hash != transaction['hash']:
                    return False
                expected_hash = hashlib.sha256((expected_hash + transaction_hash).encode()).hexdigest()
            if expected_hash != self.hash_block(block):
                return False
            previous_block = block
            block_index += 1
        return True

    # Hash a transaction
    def hash_transaction(self, transaction):
        transaction_string = json.dumps(transaction, sort_keys=True).encode()
        return hashlib.sha256(transaction_string).hexdigest()

    # Retrieve a block by its index
    def get_block_by_index(self, index):
        if index < 1 or index > len(self.chain):
            return None
        return self.chain[index - 1]

# Define the main function
def main():
    # Initialize the blockchain
    blockchain = Blockchain()

    # Define the transactions
    transaction1 = {'sender': 'John', 'receiver': 'Jane', 'amount': 10, 'hash': ''}
    transaction1['hash'] = blockchain.hash_transaction(transaction1)

    transaction2 = {'sender': 'Jane', 'receiver': 'Mark', 'amount': 5, 'hash': ''}
    transaction2['hash'] = blockchain.hash_transaction(transaction2)

    transaction3 = {'sender': 'Mark', 'receiver': 'John', 'amount': 3, 'hash': ''}
    transaction3['hash'] = blockchain.hash_transaction(transaction3)

    # Add the transactions to the blockchain
    blockchain.add_transaction(transaction1)
    blockchain.add_transaction(transaction2)
    blockchain.add_transaction(transaction3)

    # Mine a new block
    previous_block = blockchain.previous_block()
    previous_hash = blockchain.hash_block(previous_block)
    nonce = blockchain.proof_of_work()
    block = blockchain.create_block(nonce, previous_hash)

    # Check if the chain is valid
    print('Blockchain is valid:', blockchain.valid_chain())

if __name__ == '__main__':
    main()
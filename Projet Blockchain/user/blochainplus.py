import hashlib
import datetime
import json
import os

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.transactions_folder = 'transactions'

        if not os.path.exists(self.transactions_folder):
            os.makedirs(self.transactions_folder)

    def create_genesis_block(self):
        return Block(0, "01/01/2023", "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def write_transaction_to_file(self, transaction, block_index):
        hashed_block_index = hashlib.sha256(str(block_index).encode()).hexdigest()
        hashed_transaction = {
            'sender': hashlib.sha256(transaction['sender'].encode()).hexdigest(),
            'recipient': hashlib.sha256(transaction['recipient'].encode()).hexdigest(),
            'amount': hashlib.sha256(str(transaction['amount']).encode()).hexdigest(),
            'block_index': hashed_block_index,
            'timestamp': transaction['timestamp']
        }

        filename = f"{hashed_transaction['sender']}-{hashed_transaction['recipient']}-{hashed_transaction['amount']}.json"
        filepath = os.path.join(self.transactions_folder, filename)

        with open(filepath, 'w') as file:
            json.dump(hashed_transaction, file)

    def store_transactions_to_files(self):
        for block in self.chain:
            block_index = block.index
            for transaction in block.data:
                if isinstance(transaction, dict):
                    self.write_transaction_to_file(transaction, block_index)
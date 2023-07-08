import hashlib
import datetime
import json

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
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.transaction_history_file = 'transaction_history.json'

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

    def write_transaction_to_file(self, transaction):
        with open(self.transaction_history_file, 'a') as file:
            json.dump(transaction, file)
            file.write('\n')

# Exemple d'utilisation
blockchain = Blockchain()

# Créer une nouvelle transaction
transaction = {
    'sender': 'John',
    'recipient': 'Alice',
    'amount': 1.5
}

# Ajouter la transaction à la liste des données du dernier bloc
latest_block = blockchain.get_latest_block()
latest_block.data = transaction

# Ajouter le nouveau bloc à la chaîne
blockchain.add_block(latest_block)

# Écrire la transaction dans le fichier JSON
blockchain.write_transaction_to_file(transaction)


transaction = {
    'sender': 'Raph',
    'recipient': 'Toto',
    'amount': 100.0
}

latest_block = blockchain.get_latest_block()
latest_block.data = transaction

blockchain.add_block(latest_block)

blockchain.write_transaction_to_file(transaction)

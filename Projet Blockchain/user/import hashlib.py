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
        self.users_file = 'users.json'

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

    def read_users_from_file(self):
        try:
            with open(self.users_file, 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = {}
        return users

    def write_users_to_file(self, users):
        with open(self.users_file, 'w') as file:
            json.dump(users, file, indent=4)

    def create_user(self):
        full_name = input("Enter your full name: ")
        email = input("Enter your email: ")

        users = self.read_users_from_file()

        if email in users:
            print("User with this email already exists.")
            return

        users[email] = {'full_name': full_name, 'balance': 0.0}
        self.write_users_to_file(users)

    def transfer_coins(self):
        sender_email = input("Enter sender's email: ")
        recipient_email = input("Enter recipient's email: ")
        amount = float(input("Enter the amount to transfer: "))

        users = self.read_users_from_file()

        if sender_email not in users or recipient_email not in users:
            print("Invalid sender or recipient email.")
            return

        sender = users[sender_email]
        recipient = users[recipient_email]

        if sender['balance'] < amount:
            print("Insufficient balance.")
            return

        sender['balance'] -= amount
        recipient['balance'] += amount

        transaction = {
            'timestamp': str(datetime.datetime.now()),
            'sender': sender_email,
            'recipient': recipient_email,
            'amount': amount
        }

        latest_block = self.get_latest_block

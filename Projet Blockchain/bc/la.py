import hashlib
import json
import random
import string
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.users = {}
        self.transactions = []
        self.pending_transactions = []
        self.block_interval = 60  # Temps en secondes pour fermer un bloc
        self.last_block_time = time.time()

    def create_genesis_block(self):
        self.add_block(previous_hash='0')

    def add_block(self, previous_hash, miner=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.pending_transactions,
            'previous_hash': previous_hash,
            'miner': miner,
            'nonce': 0  # Nonce initial à 0
        }
        self.chain.append(block)
        self.pending_transactions = []

    def get_last_block(self):
        return self.chain[-1]

    def register_user(self, user_id):
        if user_id in self.users:
            return False  # User already registered

        # Generate keys and address
        public_key, private_key, address = generate_keys_and_address()

        # Store user data
        self.users[user_id] = {
            'public_key': public_key,
            'private_key': private_key,
            'address': address,
            'token_balance': 0  # Initialize token balance to 0
        }

        return True  # User registered successfully

    def get_user_data(self, address):
        for user_id, user_data in self.users.items():
            if user_data['address'] == address:
                return user_id, user_data
        return None, None  # User not found

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the previous hash matches
            if current_block['previous_hash'] != self.hash_block(previous_block):
                return False

            # Check if the block's hash meets the difficulty criteria
            block_hash = self.hash_block(current_block)
            if not self.check_difficulty(block_hash):
                return False

        return True

    @staticmethod
    def hash_block(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def check_difficulty(self, hash):
        difficulty = 4  # Difficulté requise pour le hash (nombre de zéros)
        return hash[:difficulty] == '0' * difficulty

    def print_blockchain(self):
        for block in self.chain:
            print("Block Index:", block['index'])
            print("Timestamp:", time.ctime(block['timestamp']))
            print("Miner:", block['miner'])
            print("Previous Hash:", block['previous_hash'])
            print("Transactions:", block['transactions'])
            print("Nonce:", block['nonce'])
            print("=" * 50)

    def save_to_file(self, filename):
        data = {
            'chain': self.chain,
            'users': self.users
        }
        with open(filename, 'w') as file:
            file.write(json.dumps(data, indent=4))

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.chain = data['chain']
            self.users = data['users']

    def add_transaction(self, sender_address, recipient_address, amount):
        if sender_address == recipient_address:
            return False  # Invalid transaction

        sender_id, sender_data = self.get_user_data(sender_address)
        recipient_id, recipient_data = self.get_user_data(recipient_address)

        if not sender_data or not recipient_data:
            return False  # Invalid sender or recipient

        if sender_data['token_balance'] < amount:
            return False  # Insufficient balance

        transaction = {
            'sender': sender_address,
            'recipient': recipient_address,
            'amount': amount
        }

        self.transactions.append(transaction)
        sender_data['token_balance'] -= amount
        recipient_data['token_balance'] += amount

        return True  # Transaction successful

    def mine_block(self, miner_address):
        if len(self.transactions) == 0:
            return False  # No transactions to mine

        last_block = self.get_last_block()
        previous_hash = self.hash_block(last_block)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions,
            'previous_hash': previous_hash,
            'miner': miner_address
        }

        # Mining - Trouver le bon nonce pour satisfaire la difficulté
        while True:
            block['nonce'] += 1
            block_hash = self.hash_block(block)
            if self.check_difficulty(block_hash):
                break

        self.chain.append(block)
        self.transactions = []
        self.last_block_time = time.time()

        return True  # Block mined successfully

    def process_pending_transactions(self):
        while len(self.transactions) > 0:
            transaction = self.transactions.pop(0)
            success = self.add_transaction(transaction['sender'], transaction['recipient'], transaction['amount'])
            if not success:
                print("Transaction failed:", transaction)

# Fonction pour générer les clés et l'adresse
def generate_keys_and_address():
    # Generate random keys
    public_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    private_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    address = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    return public_key, private_key, address

# Programme principal
if __name__ == '__main__':
    blockchain = Blockchain()

    # Charge le fichier de blockchain s'il existe, sinon crée un nouveau bloc genesis
    try:
        blockchain.load_from_file('blockchain.json')
    except FileNotFoundError:
        blockchain.create_genesis_block()

    while True:
        print("1. Se connecter avec une adresse wallet existante")
        print("2. Créer un nouveau profil utilisateur")
        print("3. Faire une transaction")
        print("4. Afficher la blockchain")
        print("5. Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            address = input("Entrez votre adresse wallet : ")
            user_id, user_data = blockchain.get_user_data(address)
            if user_data:
                print(f"Bienvenue, {user_id} !")
                print("Clé publique :", user_data['public_key'])
                print("Clé privée :", user_data['private_key'])
                print("Adresse :", user_data['address'])
                continue
            else:
                print("Adresse wallet non enregistrée.")
        elif choice == "2":
            address = input("Entrez une nouvelle adresse wallet : ")
            if blockchain.register_user(address):
                user_id, user_data = blockchain.get_user_data(address)
                print(f"Profil créé avec succès. Bonjour, {user_id} !")
                print("Clé publique :",user_data['public_key'])
                print("Clé privée :", user_data['private_key'])
                print("Adresse :", user_data['address'])
                blockchain.save_to_file('blockchain.json')
            else:
                print("L'adresse wallet est déjà enregistrée.")
        elif choice == "3":
            address = input("Entrez votre adresse wallet : ")
            user_id, user_data = blockchain.get_user_data(address)
            if user_data:
                recipient_address = input("Entrez l'adresse wallet du destinataire : ")
                amount = float(input("Entrez le montant de la transaction : "))

                success = blockchain.add_transaction(address, recipient_address, amount)
                if success:
                    print("Transaction ajoutée avec succès.")
                else:
                    print("Erreur lors de la transaction. Vérifiez les adresses et les soldes.")
            else:
                print("Adresse wallet non enregistrée.")
        elif choice == "4":
            blockchain.print_blockchain()
        elif choice == "5":
            break
        else:
            print("Option invalide.")

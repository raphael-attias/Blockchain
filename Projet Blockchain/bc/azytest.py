import hashlib
import json
import random
import string

class Blockchain:
    def __init__(self):
        self.chain = []
        self.users = {}

    def create_genesis_block(self):
        self.add_block(previous_hash='0')

    def add_block(self, previous_hash, user_id=None):
        block = {
            'index': len(self.chain) + 1,
            'transactions': [],
            'previous_hash': previous_hash,
            'user_id': user_id,
            'public_key': None,
            'private_key': None,
            'address': None
        }
        self.chain.append(block)
        return block

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

    def get_user_data(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        else:
            return None  # User not found

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the previous hash matches
            if current_block['previous_hash'] != self.hash_block(previous_block):
                return False

        return True

    @staticmethod
    def hash_block(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def print_blockchain(self):
        for block in self.chain:
            print("Block Index:", block['index'])
            print("User ID:", block['user_id'])
            print("Public Key:", block['public_key'])
            print("Private Key:", block['private_key'])
            print("Address:", block['address'])
            print("Previous Hash:", block['previous_hash'])
            print("=" * 50)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.chain, indent=4))

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.chain = json.load(file)

    def get_token_balance(self, user_id):
        if user_id in self.users:
            return self.users[user_id]['token_balance']
        else:
            return None

    def effectuer_transaction(self, sender_address, recipient_address, amount):
        sender_id, sender_data = self.get_user_data_by_address(sender_address)
        recipient_data = self.get_user_data_by_address(recipient_address)

        if sender_data and recipient_data:
            sender_balance = sender_data['token_balance']
            if sender_balance >= amount:
            # Vérification de la signature
                if self.verify_signature(sender_data['public_key'], sender_address):
                # Mettez ici votre logique de transaction
                    sender_data['token_balance'] -= amount
                    recipient_data['token_balance'] += amount

                # Récompense pour la signature valide
                    self.reward_sender(sender_id)

                    return True
        return False



    def get_user_data_by_address(self, address):
        for user_id, user_data in self.users.items():
            if user_data['address'] == address:
               return user_id, user_data
        return None, None

    def verify_signature(self, public_key, address):
        # Votre logique de vérification de signature ici
        # Comparer la signature avec le hash du bloc en utilisant la clé publique et l'adresse

        # Exemple de vérification simplifiée : Comparer la somme des caractères de la clé publique avec le hash
        signature_hash = sum(ord(c) for c in public_key + address)
        target_hash = 2 * 10  # Difficulté de hash fixée à 2
        return signature_hash >= target_hash

    def reward_sender(self, user_id):
        # Votre logique de récompense ici
        # Récompenser l'envoyeur avec une quantité fixe de tokens (2.5 dans ce cas)
        reward_amount = 2.5
        self.users[user_id]['token_balance'] += reward_amount


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
        print("1. Se connecter avec un nom d'utilisateur existant")
        print("2. Créer un nouveau profil utilisateur")
        print("3. Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            user_id = input("Entrez votre identifiant d'utilisateur : ")
            user_data = blockchain.get_user_data(user_id)
            if user_data:
                print(f"Bienvenue, {user_id} !")
                print("Clé publique :", user_data['public_key'])
                print("Clé privée :", user_data['private_key'])
                print("Adresse :", user_data['address'])
                while True:
                    print("\nMenu de transactions :")
                    print("1. Faire une transaction")
                    print("2. Voir le solde de tokens")
                    print("3. Afficher la blockchain")
                    print("4. Déconnecter")
                    transaction_choice = input("Choisissez une option : ")
                    if transaction_choice == "1":
                        recipient_address = input("Entrez l'adresse du destinataire : ")
                        amount = float(input("Entrez le montant de la transaction : "))
                        sender_address = user_data['address']

                        if blockchain.effectuer_transaction(sender_address, recipient_address, amount):
                            print("Transaction réussie.")
                        else:
                            print("Transaction échouée. Solde insuffisant, adresse invalide ou signature invalide.")

                    elif transaction_choice == "2":
                        token_balance = blockchain.get_token_balance(user_id)
                        if token_balance is not None:
                            print(f"Solde de tokens pour l'utilisateur {user_id} : {token_balance}")
                        else:
                            print("Utilisateur non trouvé.")
                    elif transaction_choice == "3":
                        blockchain.print_blockchain()
                    elif transaction_choice == "4":
                        break
                    else:
                        print("Option invalide. Veuillez choisir une option valide.")
            else:
                print("Utilisateur non enregistré.")
        elif choice == "2":
            user_id = input("Entrez un nouvel identifiant d'utilisateur : ")
            if blockchain.register_user(user_id):
                user_data = blockchain.get_user_data(user_id)
                print(f"Profil créé avec succès. Bonjour, {user_id} !")
                print("Clé publique :", user_data['public_key'])
                print("Clé privée :", user_data['private_key'])
                print("Adresse :", user_data['address'])
                blockchain.add_block(previous_hash=blockchain.hash_block(blockchain.get_last_block()), user_id=user_id)
                blockchain.save_to_file('blockchain.json')
            else:
                print("L'utilisateur est déjà enregistré.")
        elif choice == "3":
            break
        else:
            print("Option invalide.")

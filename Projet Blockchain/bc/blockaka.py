import json

class BlockZero:
    def __init__(self, filename):
        self.filename = filename

    def add_transaction(self, transaction):
        with open(self.filename, 'a') as file:
            file.write(json.dumps(transaction) + '\n')

    def close_block(self):
        with open(self.filename, 'r') as file:
            transactions = file.readlines()

        if len(transactions) > 0:
            block_filename = f"block_{int(time.time())}.json"
            with open(block_filename, 'w') as block_file:
                for transaction in transactions:
                    block_file.write(transaction)

            with open(self.filename, 'w') as file:
                pass  # Vider le fichier des transactions

            return block_filename

        return None  # Aucune transaction à fermer

# Programme principal pour Bloc Zéro
if __name__ == '__main__':
    block_zero = BlockZero('block_zero.txt')

    while True:
        transaction = {
            'sender': input("Entrez l'adresse wallet de l'expéditeur : "),
            'recipient': input("Entrez l'adresse wallet du destinataire : "),
            'amount': float(input("Entrez le montant de la transaction : "))
        }

        block_zero.add_transaction(transaction)
        print("Transaction ajoutée.")

        close_choice = input("Fermer le bloc ? (O/N) : ")
        if close_choice.upper() == 'O':
            block_filename = block_zero.close_block()
            if block_filename:
                print(f"Bloc fermé avec succès : {block_filename}")
            else:
                print("Aucune transaction à fermer.")

        continue_choice = input("Continuer ? (O/N) : ")
        if continue_choice.upper() != 'O':
            break

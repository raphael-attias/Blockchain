from crypto.publickey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

# Génération d'une paire de clés RSA
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Création d'une transaction
transaction = "Transaction data..."

# Signature de la transaction avec la clé privée
hash = SHA256.new(transaction.encode('utf-8'))
signer = PKCS1_v1_5.new(key)
signature = signer.sign(hash)

# Vérification de la signature avec la clé publique
hash = SHA256.new(transaction.encode('utf-8'))
verifier = PKCS1_v1_5.new(key.publickey())
is_valid = verifier.verify(hash, signature)

print("Clé privée:", private_key)
print("Clé publique:", public_key)
print("Signature:", signature)
print("La signature est valide:", is_valid)
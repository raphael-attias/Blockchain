from trilio import Trilio
import datetime

blockchain = Trilio()
#valid = blockchain.validate_chain() # True = Valid, False = Invalid
wallet = blockchain.Wallet.create_wallet() # Will return json with wallet information
address = wallet["address"]
address["pve"] # Private key
address["pbc"] # Public key
blockchain.Wallet.get_public_key(private_key=<private_key>)
blockchain.Wallet.credit_wallet(public_key=<public_key>, amount=<amount>)
blockchain.Wallet.validate_wallet(private_key=<private_key>, public_key=<public_key>) # True = found, False = not found
# Need to import datetime
blockchain.create_transaction(
    datetime.now(),
    data = {
        "type":"token-transfer",
        "data":{
            "to":<public_key (Wallet recieving)>,
            "from":<private_key (Wallet sending)>,
            "amount":<amount>
        }
    }
)
# Need to import datetime
blockchain.create_transaction(
    datetime.now(),
    data={
        "type":"asset-transfer",
        "data":{
            "_to":<public_key_receiver>,
            "_from":<private_key_sender>,
            "fassets":[<sending_assets_id>],
            "tassets":[<receiving_assets_id>]
        }
    }
)
# Need to import datetime
blockchain.create_transaction(
    datetime.now(),
    data={
        "type":"contract-action",
        "action":"accept-trade",
        "data":{
            "id":<trade_id>,
            "signer":<private_key>
        }
    }
)
# Need to import datetime
blockchain.create_transaction(
    datetime.now(),
    data={
        "type":"contract-action",
        "action":"decline-trade",
        "data":{
            "id":<trade_id>,
            "signer":<private_key>
        }
    }
)
# Need to import datetime
blockchain.create_transaction(
    datetime.now(),
    data = {
        "type":"contract-action",
        "action":"collection-creation",
        "data":{
            "name":<collection_name>,
            "description":<collection_description>,
            "url":<collection_url>,
            "icon":<collection_icon>,
            "tags":<collection_tags>,
            "signer":<private_key>
        }
    }
)

#print(blockchain.Wallet.get_collections(private_key=<private_key>, public_key=<public_key>))
# Need to import datetime
blockchain.create_transaction(
    datetime.now(),
    data={
        "type":"contract-action",
        "action":"asset-creation",
        "data":{
            "name":<asset_name>,
            "description":<asset_description>,
            "collection_id":<collection_id>,
            "quantity":<asset_mint_amount>,
            "signer":<private_key>
        }
    }
)

#print(blockchain.Wallet.get_assets(private_key=<private_key>, public_key=<public_key>))
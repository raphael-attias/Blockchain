from datetime import datetime
import hashlib

class Trade:
    def __init__(self, timestamp, _to, _from, fassets, tassets, tradestorage):
        self.id = len(tradestorage.trades) + 1
        self._to = _to
        self._from = _from
        self.fassets = fassets
        self.tassets = tassets
        self.state = 0  # 0 = pending, 1 = accepted, 2 = decline
        self.created_at = timestamp
        tradestorage.trades.append(self)

    def get_id(self):
        return self.id


class TradeHandler():
    def accept_trade(self, trade_id, private_key, address, assets, _ad, tradestorage):
        for trade in tradestorage.trades:
            if trade.id == trade_id:
                if trade.state == 2 or trade.state == 1:
                    return  # This trade has already been interacted with
                if trade._to == address.get_public_key(private_key):
                    tassets = 0
                    for asset_id in trade.tassets:
                        for asset in assets.assets:
                            if asset.id == asset_id and asset.owner == trade._to:
                                tassets += 1
                    if tassets == len(trade.tassets):
                        for asset_id in trade.tassets:
                            assets.assets[asset_id-1].owner = address.get_public_key(trade._from)
                            for addr in address.addresses:
                                if addr["address"]["pve"] == trade._from:
                                    addr["info"]["assets"].append(asset_id)
                            for addr in _ad.addresses:
                                if addr["address"]["pbc"] == trade._to:
                                    addr["info"]["assets"].pop(addr["info"]["assets"].index(asset_id))

                        for asset_id in trade.fassets:
                            assets.assets[asset_id-1].owner = trade._to
                            for addr in _ad.addresses:
                                if addr["address"]["pbc"] == trade._to:
                                    addr["info"]["assets"].append(asset_id)

                        trade.state = 1
                else:
                    print("wrong address")

    def decline_trade(self, trade_id, private_key, address, assets, _ad, tradestorage):
        for trade in tradestorage.trades:
            if trade.id == trade_id:
                if trade.state == 2 or trade.state == 1:
                    return  # This trade has already been interacted with
                if trade._from == private_key or trade._to == address.get_public_key(private_key):
                    for asset in assets.assets:
                        try:
                            if asset.owner["refund"] == address.get_public_key(trade._from) and asset.owner[
                                "trade_id"] == trade_id:
                                asset.owner = address.get_public_key(trade._from)
                                for _address in _ad.addresses:
                                    if _address["address"]["pve"] == trade._from:
                                        _address["info"]["assets"].append(asset.id)
                        except:
                            pass
                trade.state = 2


class CollectionHandler():
    def create_collection(self, timestamp, public_key, url, icon, name, description, tags, _ad=None, _co=None):
        collection_id = len(_co.collections) + 1
        collection = Collection(collection_id, name, description, tags, icon, url, public_key, timestamp)
        _co.collections.append(collection)
        for address in _ad.addresses:
            if address["address"]["pbc"] == public_key:
                address["info"]["collections"].append(collection_id)

    def validate_collection_name(self, name, _co):
        for collection in _co.collections:
            if collection.name == name:
                return False

        if 4 <= len(name) <= 15:
            return True
        return False

    def validate_collection_owner(self, public_key, collection_id, _co):
        for collection in _co.collections:
            if collection.id == collection_id and collection.owner == public_key:
                return True
        return False


class Asset:
    def __init__(self, timestamp, public_key, collection_id, name, description, mint_number, _ad=None, _as=None):
        asset_id = len(_as.assets) + 1
        asset = Asset(asset_id, name, description, collection_id, timestamp, public_key, mint_number+1)
        _as.assets.append(asset)
        for address in _ad.addresses:
            if address["address"]["pbc"] == public_key:
                address["info"]["assets"].append(asset_id)


class Block:
    def __init__(self, timestamp, transactions, previous_hash="", addresses="", collections="", assets="", trades="",
                 asset=""):
        self.addresses = addresses
        self.asset = asset
        self.collections = collections
        self.assets = assets
        self.trades = trades
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.get_hash()
        self.status = 0  # 0 = pending, 1 = completed
        self.complete()

    def complete(self):
        for transaction in self.transactions:
            try:
                pbc = self.addresses.get_public_key(transaction.input["data"]["from"])
                pve = transaction.input["data"]["from"]
            except:
                pass

            if transaction == "genesis block":
                return

            if transaction.input["type"] == "token-transfer":
                if float(transaction.input["data"]["amount"]) >= 0:
                    if transaction.input["data"]["to"] == pbc:
                        return
                    if self.addresses.get_balance(pve, pbc) >= float(transaction.input["data"]["amount"]):
                        self.addresses.credit_wallet(transaction.input["data"]["to"],
                                                     float(transaction.input["data"]["amount"]))
                        self.addresses.credit_wallet(pbc, -float(transaction.input["data"]["amount"]))
            elif transaction.input["type"] == "contract-action":
                if transaction.input["action"] == "collection-creation":
                    is_valid_name = CollectionHandler().validate_collection_name(transaction.input["data"]["name"],
                                                                                 self.collections)
                    if is_valid_name:
                        pbc = self.addresses.get_public_key(transaction.input["data"]["signer"])
                        CollectionHandler().create_collection(datetime.now().timestamp(), pbc,
                                                              transaction.input["data"]["url"],
                                                              transaction.input["data"]["icon"],
                                                              transaction.input["data"]["name"],
                                                              transaction.input["data"]["description"],
                                                              transaction.input["data"]["tags"], self.addresses,
                                                              self.collections)
                elif transaction.input["action"] == "asset-creation":
                    pbc = self.addresses.get_public_key(transaction.input["data"]["signer"])
                    is_collection_owner = CollectionHandler().validate_collection_owner(pbc,
                                                                                         transaction.input["data"][
                                                                                             "collection_id"],
                                                                                         self.collections)
                    if is_collection_owner:
                        for i in range(transaction.input["data"]["quantity"]):
                            Asset(datetime.now().timestamp(), pbc, transaction.input["data"]["collection_id"],
                                  transaction.input["data"]["name"], transaction.input["data"]["description"], i,
                                  self.addresses, self.assets)
                elif transaction.input["action"] == "accept-trade":
                    TradeHandler().accept_trade(transaction.input["data"]["id"],
                                                transaction.input["data"])
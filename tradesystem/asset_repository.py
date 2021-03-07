from random import randint

class AssetRepository:

    def validate_order(self, order):
        """
        Simulate the validation process by assuming that 5% of all orders are invalid.
        In reality the order should be validated first at client before being sent to the exchange.
        The exchange can still validate orders to have extra protection.
        """
        val = randint(0, 100)
        return val > 5

    def update_account_state(self, from_client_id, to_client_id, security_id, currency, fiat_amount, security_amount):
        # with transaction() as tx:
        #   try:
        #       from_acc = find_account(from_client_id)
        #       to_acc = find_account(to_client_id)
        #       from_acc.balance[currency] = from_acc.balance[currency] - fiat_amount
        #       to_acc.balance[currency] = to_acc.balance[currency] + fiat_amount
        #       from_acc.assets[asset_id] = from_acc.assets[asset_id] + asset_amount
        #       to_acc.assets[asset_id] = to_acc.assets[asset_id] - asset_amount
        #       tx.commit()  
        #       return True     
        #   except:
        #       tx.rollback()
        #       return False
        return True

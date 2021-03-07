from order_type import OrderType

class Order:

    def __init__(self, asset, currency, order_type, amount, price):
        self.asset = asset
        self.currency = currency
        self.order_type = OrderType(int(order_type))
        self.amount = int(amount)
        self.price = float(price)
        self.validate()

    
    def validate(self):
        error = ''
        if len(self.currency) != 3:
            error = error + 'Currency code is invalid. '
        if self.amount <= 0 or self.price <= 0:
            error = error + 'Amount or price must be positive.'

        if error:
            raise ValueError(error)

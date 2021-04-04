from order_type import OrderType, OrderSide

order_types = { ot.name:ot.value for ot in OrderType }
order_sides = { side.name:side.value for side in OrderSide }

class Order:

    def __init__(self, client_id, security_id, currency, order_type, order_side, amount, price):
        self.client_id = client_id
        self.security_id = security_id
        self.currency = currency
        self.order_type = OrderType(order_type if isinstance(order_type, int) else order_types[order_type])
        self.order_side = OrderSide(order_side if isinstance(order_side, int) else order_sides[order_side])
        self.amount = int(amount)
        self.price = float(price)
        self.validate()

    @property
    def key(self):
        return '/'.join([self.security_id.upper(), self.currency.upper()])

    
    def validate(self):
        error = ''
        if len(self.currency) != 3:
            error = error + 'Currency code is invalid. '
        if self.amount <= 0 or self.price <= 0:
            error = error + 'Amount and price must be positive.'

        if error:
            raise ValueError(error)


    def __str__(self):
        return f'{self.security_id}|{self.currency}|{self.order_type}|{self.order_side}|{self.amount}|{self.price}'

from order_type import OrderSide
from order_list import BuyOrderList, SellOrderList

class OrderBook:

    def __init__(self):
        self.buy_book = {}
        self.sell_book = {}

    def get_matching_order(self, order):
        is_buy_order = order.order_side is OrderSide.buy
        sec_key = order.key
        book = self.buy_book if is_buy_order else self.sell_book
        opposite_book = self.sell_book if is_buy_order else self.buy_book
        # no order in opposite side, just add this order to the book
        if opposite_book[sec_key] is None:
            order_list = self.create_new_order_list(is_buy_order) if book[sec_key] is None else book[sec_key]
            order_list.insert_order(order)
            return None
        opposite_order_list = opposite_book[sec_key]
        matched = opposite_order_list.get_matching_order(order)
        if matched is None:
            book[sec_key].insert_order(order)
            return None
        return matched

    def create_new_order_list(self, is_buy_order):
        return BuyOrderList() if is_buy_order else SellOrderList()
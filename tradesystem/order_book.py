from order_type import OrderSide
from order_list import BuyOrderList, SellOrderList

class OrderBook:

    def __init__(self):
        self.buy_book = {}
        self.sell_book = {}

    def get_matching_order(self, order, reply_queue_name):
        is_buy_order = order.order_side is OrderSide.buy
        sec_key = order.key
        book = self.buy_book if is_buy_order else self.sell_book
        opposite_book = self.sell_book if is_buy_order else self.buy_book
        # no order in opposite side, just add this order to the book
        if sec_key not in opposite_book:
            self.add_order_to_book(order, book, reply_queue_name)
            return None
        opposite_order_list = opposite_book[sec_key]
        matched = opposite_order_list.get_matching_order(order)
        if matched is None:
            self.add_order_to_book(order, book, reply_queue_name)
            return None
        return matched

    def create_new_order_list(self, is_buy_order):
        return BuyOrderList() if is_buy_order else SellOrderList()

    def add_order_to_book(self, order, book, notfication_queue):
        order_list = self.create_new_order_list(order.order_side is OrderSide.buy) if order.key not in book else book[order.key]
        order_list.insert_order(order, notfication_queue)
        book[order.key] = order_list
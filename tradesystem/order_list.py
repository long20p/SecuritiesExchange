from order_type import OrderType


class OrderNode:

    def __init__(self, order, notfication_queue):
        self.order = order
        self.notfication_queue = notfication_queue
        self.next = None
        self.previous = None


class OrderList:

    def __init__(self):
        self.head = None

    def can_insert_order(self, order, next_order_in_list):
        pass

    def can_match_price(self, current_order_in_list, opposite_order):
        pass

    def get_matching_order(self, opposite_order):
        if self.head is None:
            return None
        if opposite_order.order_type is OrderType.limit:
            if not self.can_match_price(self.head.order, opposite_order) or self.head.order.amount != opposite_order.amount:
                return None
            else
                matched = self.head
                self.head = self.head.next
                return matched
        elif opposite_order.order_type is OrderType.market:
            current = self.head
            while current is not None:
                if current.order.amount == opposite_order.amount:
                    matched = current
                    if matched.previous is not None:
                        matched.previous.next = matched.next
                    if matched.next is not None:
                        matched.next.previous = matched.previous
                    return matched
                current = current.next
            return None

    def insert_order(self, order, notfication_queue):
        newNode = OrderNode(order, notfication_queue)
        current = self.head
        last = None
        while current is not None:
            if self.can_insert_order(order, current.order):
                break
            last = current
            current = current.next
        if last is not None:
            last.next = newNode
            newNode.previous = last
        else:
            self.head = newNode
        if current is not None:
            newNode.next = current
            current.previous = newNode


class BuyOrderList(OrderList):

    def can_insert_order(self, order, next_order_in_list):
        return order.price > next_order_in_list.price

    def can_match_price(self, current_order_in_list, opposite_order):
        return current_order_in_list.price >= opposite_order.price


class SellOrderList(OrderList):

    def can_insert_order(self, order, next_order_in_list):
        return order.price < next_order_in_list.price

    def can_match_price(self, current_order_in_list, opposite_order):
        return current_order_in_list.price <= opposite_order.price




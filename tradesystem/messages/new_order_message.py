from order import Order


class NewOrderMessage:

    def __init__(self, order, reply_queue_name):
        self.order = order
        self.reply_queue_name = reply_queue_name

    @staticmethod
    def toObject(**props):
        reply_queue_name = props['reply_queue_name']
        order = Order(**props['order'])
        return NewOrderMessage(order, reply_queue_name)
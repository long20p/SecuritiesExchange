class NewOrderMessage:

    def __init__(self, order, reply_queue_name):
        self.order = order
        self.reply_queue_name = reply_queue_name


    
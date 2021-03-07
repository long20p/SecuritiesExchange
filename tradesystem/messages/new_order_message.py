class NewOrderMessage:

    def __init__(self, order, client_id, reply_queue_name):
        self.order = order
        self.client_id = client_id
        self.reply_queue_name = reply_queue_name


    
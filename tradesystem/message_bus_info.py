class MessageBusInfo:

    @staticmethod
    def new_order_queue_name():
        return 'new_order_queue'

    @staticmethod
    def cancel_order_queue_name():
        return 'cancel_order_queue'
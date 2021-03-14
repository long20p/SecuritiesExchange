import pika
import json
import sys
from messages.new_order_message import NewOrderMessage
from messages.message_bus_info import MessageBusInfo
from order import Order
from order_type import OrderType, OrderSide
from order_book import OrderBook
from order_list import OrderNode
from asset_repository import AssetRepository

class Exchange:

    def __init__(self, connectionString, asset_repo, order_book):
        self.asset_repo = asset_repo
        self.order_book = order_book
        self.connection = pika.BlockingConnection(pika.URLParameters(connectionString))
        self.channel = self.connection.channel()
        new_order_queue_name = MessageBusInfo.new_order_queue_name()
        cancel_order_queue_name = MessageBusInfo.cancel_order_queue_name()
        self.channel.queue_declare(queue=new_order_queue_name)
        self.channel.queue_declare(queue=cancel_order_queue_name)
        self.channel.basic_consume(queue=new_order_queue_name, auto_ack=True, on_message_callback=self.new_order_received)
        self.channel.basic_consume(queue=cancel_order_queue_name, auto_ack=True, on_message_callback=self.cancel_order_received)
        print('Ready to accept order')


    def new_order_received(self, channel, method, props, body):
        message_dict = json.loads(body)
        message = NewOrderMessage.toObject(**message_dict)
        order = message.order
        reply_queue_name = message.reply_queue_name
        # check if order can be processed
        if self.asset_repo.validate_order(order):
            self.match_order_or_add_to_book(order, reply_queue_name)
        else:
            self.handle_invalid_order(order, reply_queue_name)


    def cancel_order_received(self, channel, method, props, body):
        pass


    def match_order_or_add_to_book(self, order, reply_queue_name):
        matched = self.order_book.get_matching_order(order, reply_queue_name)
        if matched:
            self.channel.basic_publish(exchange='', routing_key=reply_queue_name, body=f'Order matched. {str(order)}')
            # also notify the other party
            self.channel.basic_publish(exchange='', routing_key=matched.notification_queue, body=f'Order matched. {str(matched.order)}')
            # update status in asset repository
            self.asset_repo.update_account_state(order.client_id, matched.order.client_id,  
                                                 order.security_id, order.currency, 
                                                 order.amount * matched.order.price, order.amount)
            print(f'Matched orders between {order.client_id} and {matched.order.client_id}')

    def handle_invalid_order(self, order, reply_queue_name):
        error = 'Insufficent fund to buy' if order.order_side is OrderSide.buy else 'Insufficient assets to sell'
        self.channel.basic_publish(exchange='', routing_key=reply_queue_name, body=f'{error}. Order {str(order)}')


    def run(self):
        self.channel.start_consuming()



if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Must provide message queue endpoint')
    exchange = Exchange(sys.argv[1], AssetRepository(), OrderBook())
    exchange.run()
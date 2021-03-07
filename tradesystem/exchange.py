import pika
import json
import sys
from messages.new_order_message import NewOrderMessage
from message_bus_info import MessageBusInfo
from order import Order
from order_book import OrderBook
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
        self.channel.basic_consume(queue=new_order_queue_name, on_message_callback=self.new_order_received)
        self.channel.basic_consume(queue=cancel_order_queue_name, on_message_callback=self.cancel_order_received)

    def new_order_received(self, channel, method, props, body):
        pass

    def cancel_order_received(self, channel, method, props, body):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Must provide message queue endpoint')
    exchange = Exchange(sys.argv[1], AssetRepository(), OrderBook())
    exchange.run()
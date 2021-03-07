import pika
import sys
from message_bus_info import MessageBusInfo
from order import Order
from messages.new_order_message import NewOrderMessage
from messages.message_serializer import MessageSerializer

promptText = 'Enter order (asset currency orderType amount price):'


class ExchangeClient:

    def __init__(self, clientId, connectionString):
        self.id = clientId
        self.serializer = MessageSerializer()
        self.connection = pika.BlockingConnection(pika.URLParameters(connectionString))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=MessageBusInfo.new_order_queue_name())
        self.channel.queue_declare(queue=MessageBusInfo.cancel_order_queue_name())
        self.reply_queue = self.channel.queue_declare(queue='', exclusive=True)
        self.channel.basic_consume(queue=self.reply_queue.method.queue,
                                   auto_ack=True, on_message_callback=self.on_notification_received)

    def on_notification_received(self, channel, method, props, body):
        print(body)

    def create_order(self, order_info):
        tokens = order_info.split()
        if len(tokens) != 5:
            print('ERROR: Wrong number of arguments')
        else:
            try:
                order = Order(*tokens)
                message = NewOrderMessage(order, self.id, self.reply_queue.method.queue)
                serializedMsg = self.serializer.encode(message)
                print(serializedMsg)
                self.channel.basic_publish(exchange='', routing_key='', body=serializedMsg)
                print('Order sent')
            except Exception as e:
                print(f'ERROR: {str(e)}')


def execute():
    if len(sys.argv) != 3:
        raise Exception('Must provide client ID and message queue endpoint')
    client = ExchangeClient(sys.argv[1], sys.argv[2])
    line = input(promptText)
    while line:
        client.create_order(line)
        line = input(promptText)


if __name__ == '__main__':
    execute()
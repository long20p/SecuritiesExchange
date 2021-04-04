import pika
import sys
import threading
from messages.message_bus_info import MessageBusInfo
from order import Order
from messages.new_order_message import NewOrderMessage
from messages.message_serializer import MessageSerializer

promptText = 'Please start entering order information (asset currency orderType orderSide amount price)'

class ClientReplyThread(threading.Thread):

    def __init__(self, reply_queue, channel):
        self.channel = channel
        self.channel.basic_consume(queue=reply_queue,
                                   auto_ack=True, on_message_callback=self.on_notification_received)
        super(ClientReplyThread, self).__init__()
        self.start()

    def run(self):
        self.channel.start_consuming()

    def on_notification_received(self, channel, method, props, body):
        print(body)


class ExchangeClient:

    def __init__(self, clientId, connectionString):
        self.id = clientId
        self.serializer = MessageSerializer()
        self.connection = pika.BlockingConnection(pika.URLParameters(connectionString))
        self.channel = self.connection.channel()
        self.new_order_queue_name = MessageBusInfo.new_order_queue_name()
        self.cancel_order_queue_name = MessageBusInfo.cancel_order_queue_name()
        self.channel.queue_declare(queue=self.new_order_queue_name)
        self.channel.queue_declare(queue=self.cancel_order_queue_name)
        self.reply_queue = self.channel.queue_declare(queue='', exclusive=True)
        self.reply_thread = ClientReplyThread(self.reply_queue.method.queue, self.channel)

    def create_order(self, order_info):
        tokens = order_info.split()
        if len(tokens) != 6:
            print('ERROR: Wrong number of arguments')
        else:
            try:
                order = Order(self.id, *tokens)
                message = NewOrderMessage(order, self.reply_queue.method.queue)
                serializedMsg = self.serializer.encode(message)
                print(serializedMsg)
                self.channel.basic_publish(exchange='', routing_key=self.new_order_queue_name, body=serializedMsg)
                print('Order sent')
            except Exception as e:
                print(f'ERROR: {str(e)}')

    def on_exit(self):
        self.connection.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception('Must provide client ID and message queue endpoint')
    client = ExchangeClient(sys.argv[1], sys.argv[2])
    print(promptText)
    line = input()
    while line:
        client.create_order(line)
        line = input()
    client.on_exit()
# SecuritiesExchange
A simple demonstration of basic components of an exchange. Message queue is used for communication.

## Prerequisites
- RabbitMQ server is up and running somewhere accessible. Some companies provide RabbitMQ as-a-service e.g. CloudAMQP.
- Copy the endpoint URL in the form of amqp://[username]:[password]@[hostname]/[instancename]

## Run exchange
`python exchange.py [RabbitMQ endpoint]`
- The exchange will listen for new orders and try to match them with existing ones
- If an order cannot be matched it will be added to the order book

## Run client
`python client.py [client ID] [RabbitMQ endpoint]`
- client ID is any string that uniquely identifies a client
- Multiple clients can run at the same time
### Create new order
- Enter 6 pieces of information for an order: `[security_id] [currency] [order_type] [order_side] [amount] [price]`
- Example: `AAPL USD market buy 500 127.36`
- Possible values for order_type: market, limit
- Possible values for order_side: buy, sell

## Considerations for improvements
- Cancel order that hasn't been matched
- Specify security type: stock, bond, cryto, derivative etc.
- Currently the trade system only accepts buying/selling securities for fiat currencies. If any kind of transaction is allowed then 2 different order books (buy/sell) can be merged into 1.
- Examples of possible pairs: stock/fiat, crypto/fiat, crypto/crypto, stock/crypto

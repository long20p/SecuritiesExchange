from enum import IntEnum

class OrderType(IntEnum):
    market = 1
    limit = 2
    #stop = 3


class OrderSide(IntEnum):
    buy = 1
    sell = 2
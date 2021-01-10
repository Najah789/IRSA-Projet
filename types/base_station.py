
from enum import Enum
class Ack(Enum):
    RECEIVED = 0.9
    NOT_SINGLE = 0.4
    NOT_RECEIVED = 0.1

class BaseStation(object):
    """
    Base Station
    """
    def __init__(self) -> None:
        super().__init__()
        self.ack = Ack(None)

    ## To be continued..
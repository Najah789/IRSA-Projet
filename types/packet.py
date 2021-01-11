
class Packet(object):
    """
    Packet
    """
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    def __str__(self) -> str:
        return self.value

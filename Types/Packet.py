
class Packet(object):
    """
    Packet
    """
    def __init__(self, value=None) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return self.value

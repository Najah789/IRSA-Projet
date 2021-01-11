class Slot(object):
    """
    Slot
    """
    SLOT_NUMBER = 0 # static number defining the total number of slots
    def __init__(self) -> None:
        super().__init__()
        self.index = Slot.SLOT_NUMBER
        self.packets = list()   # list of packets
        self.chosen = False

        Slot.SLOT_NUMBER += 1



    def __str__(self) -> str:
        return f"Slot {self.index})\n\tPacket: {self.packet}"

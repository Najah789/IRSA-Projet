from Types.Packet import Packet


class Slot(object):
    """
    Slot class
    """
    SLOT_COUNT = 0 # static number defining the total number of slots
    def __init__(self) -> None:
        super().__init__()
        self.index = Slot.SLOT_COUNT
        self.packets = list()   # list of packets

        Slot.SLOT_COUNT += 1

    def add_packet(self, packet:Packet):
        """
        This function ads a received packet
        """
        self.packets.append(packet)

    def __str__(self) -> str:
        return f"Slot {self.index})\n\tPacket: {self.packet}"


class Machine(object):
    """
    Machine class
    """
    MACHINE_COUNT = 0 # static number defining the total number of initiated machines 
    def __init__(self, packets=None):
        self.index = Machine.MACHINE_COUNT
        if packets is None:
            self.packets = []
        else:
            self.packets = packets

        Machine.MACHINE_COUNT += 1

    def add_packet(self, packet):
        """
        This function adds a packet into the list of packets
        """
        self.packets.append(packet)

    
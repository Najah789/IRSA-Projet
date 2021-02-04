# This class is a python package

import random, string
from enum import Enum

MAX_NUM_OF_SLOTS = 10

class Ack(Enum):
    RECEIVED = 0.9
    NOT_SINGLE = 0.4
    NOT_RECEIVED = 0.1


class Packet(object):
    """
    Packet class
    """
    def __init__(self, value=None) -> None:
        super().__init__()
        
        # Attributing a random caracter as a value for the packet
        self.value = ''.join(random.choice(string.ascii_letters))
        # If the value is passed in the parameters, attribute that instead
        if value:
            self.value = value
   
    def __repr__(self) -> str:
        return self.value


class Frame(object):
    """
    Frame class (c'est la Trame en français)
    """
    COUNT = 0 # static number defining the total number of initiated machines 
    
    def __init__(self):
        self.index = Frame.COUNT
        # create a list of empty slots
        self.slots = [[] for _ in range(MAX_NUM_OF_SLOTS)]

        Frame.COUNT += 1
    
    def receive_packet(self, packet:Packet):
        """
        This functions assings a reveived packet to a slot.
        The slot will be chosen randomly.
        """
        index = random.randint(0, 9)
        self.slots[index].append(packet)

    def __repr__(self) -> str:
        r = f'Frame {self.index} | \t'
        for slot in self.slots:
            r += ''.join(str(slot))
        r += '\n'
        return r


class BaseStation(object):
    """
    Base Station
    """
    def __init__(self) -> None:
        super().__init__()


    ## TODO


class Equipment(object):
    """
    Equipment class
    """
    COUNT = 0 # static number defining the total number of initiated machines 
    
    def __init__(self, packets_count=None, distribution_times=None):
        self.index = Equipment.COUNT

        self.distribution_times = distribution_times

        # Create a list of packets
        self.packets = [Packet() for _ in range(packets_count)]

        Equipment.COUNT += 1

    def send_packets(self, frame:Frame):
        for packet in self.packets:
            self.__send_packet(packet, frame)

    def __send_packet(self, packet:Packet, frame:Frame):
        # we choose the number of copies (k)
        k = random.randint(1, 3)
        for _ in range(k):
            frame.receive_packet(packet)
        

    def __repr__(self) -> str:
        return f"Packets\t>\tDitribution Times\n{str(self.packets)}\t>\t{str(self.distribution_times)}\n"

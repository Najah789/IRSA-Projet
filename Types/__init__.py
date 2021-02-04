# This class is a python package

import random, string, math

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
    COUNT = 0 # static number defining the total number of frames 
    
    def __init__(self, index=None):
        if index == None:
            self.index = Frame.COUNT
        else:
            self.index = index

        # create a list of empty slots
        self.slots = [[] for _ in range(MAX_NUM_OF_SLOTS)]

        Frame.COUNT += 1
    
    def receive_packet(self, packet:Packet, slot_id:int=-1):
        """
        This functions assings a reveived packet to a slot.
        """
        if slot_id < 0:
            # choose randomly
            index = random.randint(0, 9)
            self.slots[index].append(packet)
        else:
            # assign directly
            self.slots[slot_id].append(packet)

    def __repr__(self) -> str:
        r = f'Frame {self.index} | \t'
        for slot in self.slots:
            r += ''.join(str(slot))
        r += '\n'
        return r


class BaseStation(object):
    """
    Base Station class
    """
    def __init__(self):
        self.frames_poisson = []
        self.frames_random = []
        self.__broadcast_frame = None

    def detect_collisions(self, is_poisson:bool=False):
        # TODO: COLLISION DETECTION GOES HERE
        # 1. detect if there are any collisions in between frames ~ slots
        # 2. Merge the slots of the all frames into  the broadcast_frame
        # 3. Reward equipment if any (TODO: implementation of rewarding system)
        # 4. Calculate packet loss
        pass

class Equipment(object):
    """
    Equipment class
    """
    COUNT = 0 # static number defining the total number of initiated machines 
    
    def __init__(self, packets_count=None, dist:list=None):
        self.index = Equipment.COUNT

        if dist:
            self.distribution_times:list = dist
            self.__normalize_dist()

        # Create a list of packets
        self.packets = [Packet() for _ in range(packets_count)]

        Equipment.COUNT += 1

    def set_distribution(self, dist:list):
        self.distribution_times = dist
        self.__normalize_dist()

    def send_packets(self, frame:Frame, is_poisson:bool=False):
        for i, packet in enumerate(self.packets):
            if not is_poisson:
                # send packet to a random slot
                self.__send_packet(packet, frame)
            else:
                # send packet to the slot indexed by 't' (POISSON)
                t = self.distribution_times[i]
                self.__send_packet(packet, frame, t)

    def __send_packet(self, packet:Packet, frame:Frame, slot_id:int=-1):
        # we choose the number of copies (k)
        k = random.randint(2, 4)
        for _ in range(k):
            frame.receive_packet(packet, slot_id)
        
    def __normalize_dist(self):
        min_v = min(self.distribution_times)
        max_v = max(self.distribution_times)

        for i, v in enumerate(self.distribution_times):
            self.distribution_times[i] =  math.floor((MAX_NUM_OF_SLOTS-1) * ((v - min_v)/(max_v - min_v)))

    def __repr__(self) -> str:
        return f"Packets\t>\tDitribution Times\n{str(self.packets)}\t>\t{str(self.distribution_times)}\n"

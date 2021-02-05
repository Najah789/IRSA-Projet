# This class is a python package

import random, string, math

from enum import Enum

MAX_NUM_OF_SLOTS = 100

class Ack(Enum):
    RECEIVED = 0.9
    MULTIPLE = 0.4
    COLLISION = 0.1


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
    def __init__(self, total_packets):
        self.frames_poisson = []
        self.frames_random = []
        self.__broadcast_frame = Frame(-1)

        self.__total_packets = total_packets

    @property
    def bf(self):
        return self.__broadcast_frame

    def detect_collisions(self, is_poisson:bool=False) -> list:
        """
            This function detects collisions and returns a table of boolean
            of the occured collisions
        """
        # detect if there are any collisions in between frames ~ slots
        collision_table = [Ack.COLLISION for _ in range(MAX_NUM_OF_SLOTS)]
        frames = self.frames_poisson.copy()
        if not is_poisson:
            frames = self.frames_random.copy()
        
        for i in range(MAX_NUM_OF_SLOTS):
            # check for collision and return slot
            (frame, slot, ret) = self.__check_for_collision(frames, i)

            # update collision table
            collision_table[i] = ret

            # if there is not a collision
            if ret != Ack.COLLISION:
                # we remove all packets of the slot from the whole frame
                self.__remove_packets_from_frame(slot, frame)
                # add the slot to the the broadcast frame
                self.__broadcast_frame.slots[i] = slot
            else:
                # add an empty slot
                self.__broadcast_frame.slots[i] = []

        return collision_table

    def __check_for_collision(self, frames:list, index:int) -> tuple:
        """
            This function returns checks and return a tuple frame, slot and ret
        """
        slot = None
        frame = None
        ret = Ack.COLLISION
        count = 0
        for f in frames:
            slots = f.slots 
            if len(slots[index]) >= 1:
                slot = slots[index]
                frame = f
                ret = Ack.RECEIVED
                count += 1
            if count > 1:
                slot = None
                frame = None
                ret = Ack.COLLISION
                break

        if slot != None and len(slot) > 1:
            ret = Ack.MULTIPLE

        return (frame, slot, ret)

    def __remove_packets_from_frame(self, slot:list, frame:Frame):
        """
            This function removes given packets from a frame
        """
        for s in frame.slots:
            for packet in slot:
                if packet in s:
                    s.remove(packet)

    def print_ratios(self):
        packets_received = 0
        for slot in self.__broadcast_frame.slots:
            temp = list(dict.fromkeys(slot))
            packets_received += len(temp)

        packets_not_received = self.__total_packets - packets_received

        packet_loss = packets_not_received / self.__total_packets
        
        print("packet loss: {:0.2f} %".format((packet_loss*100)))
    
    def clear(self):
        self.__broadcast_frame = Frame(-1)


class Equipment(object):
    """
    Equipment class
    """
    COUNT = 0 # static number defining the total number of initiated machines 
    
    def __init__(self, packets_count=None, dist:list=None):
        self.index = Equipment.COUNT
        self.gain_tab = []

        if dist:
            self.distribution_times:list = dist
            self.__normalize_dist()

        # Create a list of packets
        self.packets = [Packet() for _ in range(packets_count)]

        Equipment.COUNT += 1

#*******************************************************************************
    def __send_packet_rand_dist(self, frame:Frame, nbr_slot:int):
        # we test for all the possible copies
        for _ in range(0, nbr_slot):
            slot_id = random.randint(0, 9)
            for packet in enumerate(self.packets):
                # send packet to the slot indexed by 'slot_id'
                self.__send_packet_rand(packet, frame, slot_id)

    def __send_packet_rand(self, packet:Packet, frame:Frame, slot_id):
        # we choose the number of copies (k)
        k = random.randint(1, 10)
        for _ in range(k):
            frame.receive_packet(packet, slot_id)

    def __rand_dist(self, frame:Frame):
        for i in range(1, 11):
            self.__send_packet_rand_dist(frame, i)

#**********************************************************************************

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

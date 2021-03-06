# This class is a python package

import random, string, math

from enum import Enum

MAX_NUM_OF_SLOTS = 10
TESTS_COUNT = 1000


class Ack(Enum):
    RECEIVED = 0.9
    MULTIPLE = 0.4
    COLLISION = 0.1
    EMPTY = 0


class Packet(object):
    """
    Packet class
    """
    def __init__(self, value=None, equipment=None) -> None:
        super().__init__()
        self.equipment = equipment
        
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
    
    def receive_packet(self, packet:Packet, slot_id:int):
        """
        This functions assings a reveived packet to a slot.
        """
        # assign directly
        self.slots[slot_id].append(packet)

    def __repr__(self) -> str:
        r = f'Frame {self.index} | \t'
        for slot in self.slots:
            r += ''.join(str(slot))
        return r


class Equipment(object):
    """
    Equipment class
    """
    COUNT = 0 # static number defining the total number of initiated machines 
    
    def __init__(self, packets_count=None, frame:Frame=None):
        self.index = Equipment.COUNT
        # initialize gain_tab
        self.gain_tab = [0 for _ in range(MAX_NUM_OF_SLOTS)]
        self.tests_count = 0
        self.frame = frame

        # Create a list of packets
        self.packets = [Packet(equipment=self) for _ in range(packets_count)]

        Equipment.COUNT += 1

    # Initialisation trames (UCB1)
    def rand_dist(self, strategy:int):
        self.frame = Frame(index=self.index)
        self.__send_packet_rand_dist(self.frame, strategy)

    def __send_packet_rand_dist(self, frame:Frame, nbr_slot:int):
        # we test for all the possible copies
        for _ in range(nbr_slot):
            slot_id = random.randint(0, MAX_NUM_OF_SLOTS-1)
            for packet in self.packets:
                # send packet to the slot indexed by 'slot_id'
                self.__send_packet_rand(packet, frame, slot_id)

    def __send_packet_rand(self, packet:Packet, frame:Frame, slot_id:int):
        # we choose the number of copies (k)
        k = random.randint(2, 4)
        for _ in range(k):
            frame.receive_packet(packet, slot_id)

    def __choose_slots(self, strategy:int) -> list:
        """
        This functions chooses randomly the number of slots
        and the return a list of the chosen slots
        """
        chosen_id_slots = []
        for _ in range(strategy):
            slot_id = random.randint(0, MAX_NUM_OF_SLOTS-1)
            while slot_id in chosen_id_slots:
                slot_id = random.randint(0, MAX_NUM_OF_SLOTS-1)
            chosen_id_slots.append(slot_id)
        return chosen_id_slots

    # Poisson 
    def __get_copies_count(self, lmbd:float) -> int:
        r = random.uniform(0,1)
        t = -math.log(r) / lmbd
        return math.ceil(t)

    def send_packets(self, lmbd:float, strategy:int):
        """
        This functions sends all packets to it's frame
        """
        self.frame = Frame(index=self.index)
        slots_id = self.__choose_slots(strategy)
        for packet in self.packets:
            for slot in slots_id:
                self.__send_packet(packet, slot, lmbd)

    def __send_packet(self, packet:Packet, slot_id:int, lmbd:float):
        # choose the copies count by Poisson
        k = self.__get_copies_count(lmbd)
        for _ in range(k):
            self.frame.receive_packet(packet, slot_id)

    def __repr__(self) -> str:
        return f"Equipment {self.index}\n\
            # Packets\t{str(self.packets)}\n\
            {str(self.frame)}\n\
            Gain Tab\t{str(self.gain_tab)}"


class BaseStation(object):
    """
    Base Station class
    """
    def __init__(self, total_packets):
        self.frames_poisson = []
        self.equipments = None
        self.__broadcast_frame = Frame(-1)

        self.__total_packets = total_packets

    @property
    def bf(self):
        return self.__broadcast_frame

    def set_equipments(self, equipments:list):
        self.equipments = equipments
    
    def detect_collisions(self) -> list:
        """
        This function detects collisions and returns 
        a table of boolean of the occured collisions
        """
        collision_table = [Ack.EMPTY for _ in range(MAX_NUM_OF_SLOTS)]
        
        # detect if there are any collisions in between equipments ~ frames ~ slots
        for i in range(MAX_NUM_OF_SLOTS):
            # check for collision and return slot
            (equipment, slot, ack) = self.__check_for_collision(i)

            if equipment != None:
                # update collision table
                collision_table[i] = ack

            # if there is not a collision
            if ack != None and ack != Ack.COLLISION:
                # we remove all packets of the slot from the whole frame
                self.__remove_packets_from_frame(slot, equipment.frame)
                # add the slot to the the broadcast frame
                self.__broadcast_frame.slots[i] = slot
            else:
                # add an empty slot
                self.__broadcast_frame.slots[i] = []

        return collision_table

    def __check_for_collision(self, index:int) -> tuple:
        """
        This function returns checks and return a tuple equipment, slot and ack
        """
        slot = None
        equipment = None
        collided_equipments = []
        ack = None

        for e in self.equipments:
            tmp = e.frame.slots[index]
            is_empty_slot = len(tmp) <= 0

            if is_empty_slot:
                continue

            if not is_empty_slot:
                equipment = e
                collided_equipments.append(e)
                slot = tmp
                ack = Ack.RECEIVED

        if len(collided_equipments) > 1:
            ack = Ack.COLLISION
            slot = None
            # reward equipments by 0.1
            for e in collided_equipments:
                self.__reward_equipment(e, ack, index)

        if slot != None and len(slot) > 1:
            ack = Ack.MULTIPLE
        
        # reward equipment
        if ack != None and ack != Ack.COLLISION:
            self.__reward_equipment(equipment, ack, index)

        return (equipment, slot, ack)

    def __reward_equipment(self, equipment:Equipment, ack:Ack, slot_id:int):
        equipment.gain_tab[slot_id] = ack.value

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
        Equipment.COUNT = 0

from . import Slot
from . import Packet

from constants import MAX_NUM_OF_SLOTS

import random

class Trame(object):
    """
    Trame class
    """
    def __init__(self):
        self.slots = list()
        for _ in range(MAX_NUM_OF_SLOTS):
            self.slots.append(Slot())
        
    def add_slot(self, slot:Slot):
        """
        This function add a slot into the list of slots
        """
        if type(slot) is Slot:
            self.slots.append(slot)

    def receive_packet(self, packet:Packet):
        """
        This functions assings a reveived packet to a slot.
        The slot will be chosen randomly.
        """
        for slot in self.slots:
            r = random.random()
            if r <= 0.1:    # 10% chance
                slot.add_packet(packet)
                print(f"packet assigned to slot {slot.index}")

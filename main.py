"""
    Title:      Irregular Repetition Slotted Aloha (IRSA)
    Authors:    AZZAHRAOUI Najah
                BEN MABROUK Houssem
    Year:       2021 / 2022
"""

from Types import BaseStation
from Types import Equipment
from Types import Packet
from Types import Frame

import random
import math
import time

def get_distrubtion_times(lmbd:float):
    times = []
    
    old_t = 0
    for _ in range(packets_count):
        r = random.uniform(0,1)
        t = -math.log(r) / lmbd
        
        times.append(old_t + t)
        old_t += t
    return times

if __name__ == "__main__":

    # Input for equipment count
    equipments_count = -1
    while equipments_count < 0 or equipments_count > 20:
        try:
            equipments_count = input("Enter how many equipements are there (default = 10): ")
            if not equipments_count:
                equipments_count = 10
            else:
                equipments_count = int(equipments_count)
        except ValueError:
            print("Error: must be an integer! (10 <= number <= 20)")
        if equipments_count < 0 or equipments_count > 20:
            print("Warning: must be a number between 10 and 20")

    # Input for how many packets will be sent by equipment
    packets_count = -1
    while packets_count <= 1:
        try:
            packets_count = int(input("Enter the number of packets each equipment will send: "))
        except ValueError:
            print("Error: must be an integer! (> 1)")
        if packets_count <= 1:
            print("Warning: must be a number greater than 1")
    
    # Input for lambda value
    lmbd = -1
    while lmbd <= 0 or lmbd > 2:
        try:
            lmbd = input("Enter the lambda value (default = 0.5): ")
            if not lmbd:
                lmbd = 0.5
            else:
                lmbd = float(lmbd)
        except ValueError:
            print("Error: must be a float! (0 < lambda <= 2)")
        if lmbd < 0 or lmbd > 2:
            print("Warning: must be a number between 0 and 2")
    
    # Create the Base Station
    bs = BaseStation(packets_count)

    # Simulation run for 100 simulation frame
    for _ in range(100):
        # Create a list of equipments
        equipments = []
        for _ in range(equipments_count):
            e = Equipment(packets_count)
            e.set_distribution(get_distrubtion_times(lmbd))
            equipments.append(e)
        
        # Create a list of frames
        bs.frames_poisson = [Frame(index=i) for i in range(equipments_count)]
        bs.frames_random = [Frame(index=i) for i in range(equipments_count)]

        for i, e in enumerate(equipments):
            e.send_packets(bs.frames_poisson[i], True)
            e.send_packets(bs.frames_random[i], False)
        
        x = bs.detect_collisions(True)
        bs.print_ratios()

        bs.clear()

        input()

    # TODO Implementation of UCB1 using MAB
    # TODO Drawing plots of performance

    ## GENERAL INFORMATIONS
    # the packets arrives following Poisson using parameter LAMBDA
    # the equipment chooses randomly k SLOTs from the 10 SLOTs
    #   k : random between 1 and 3
    
    ## GUIDELINE
    # 1) equipment sends packets to BS
    # sends multiple copies of it's packet in a frame that has 10 SLOTs
    # 2) a collision is when two equipments or more sends their packet to the same SLOT
    # 3) if a packet didn't collide with another packet
    # BS eliminates this copie from frame
    # ...

    """ EXAMPLE
        D'aprés les videos en ligne (https://youtu.be/RN4XKqTEjDA)

        S represents a slot
        X represents a frame (trame en français :p)
        C represents a collision

        |------------|S (1)|S (2)|S (3)|S (4)|S (5)|S (6)|S (7)|S (8)|S (9)|S(10)|
        |EQUIPMENT 1 |--X--|-----|--X--|-----|--X--|-----|-----|--X--|-----|--X--| <- Frame 1
        |EQUIPMENT 2 |--X--|-----|-----|--X--|-----|-----|-----|-----|--X--|-----| <- Frame 2
        |EQUIPMENT 3 |-----|--X--|-----|-----|--X--|-----|--X--|-----|--X--|-----| <- Frame 3
        |------------|-----------------------------------------------------------|
        |BROADCAST   |--C--|--X--|--X--|--X--|--C--|-----|--X--|--X--|--C--|--X--| <- Frame of BS ?
        |------------|-----------------------------------------------------------|
    """

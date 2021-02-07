"""
    Title:      Irregular Repetition Slotted Aloha (IRSA)
    Authors:    AZZAHRAOUI Najah
                BEN MABROUK Houssem
    Year:       2021 / 2022
"""

from Types import BaseStation
from Types import Equipment
from Types import Frame

from Types import TESTS_COUNT
import matplotlib.pyplot as plt

import random
import math


# UCB1 
def UCB1(equipments:list):
    overall_number_tests = 1
    ucb_previous = 0
    ucb = 0
    for _ in range(TESTS_COUNT):
        for eq in equipments:
            eq.tests_count += 1
            x = sum(eq.gain_tab) / len(eq.gain_tab)
            ucb = x + math.sqrt((2*math.log(overall_number_tests)) / eq.tests_count)
            ucb = max(ucb, ucb_previous)
            ucb_previous = ucb
            overall_number_tests += 1
    return ucb

def graph_plot(irsa_tab:list, ucb_tab:list, nbr_eq):
    plt.hist([irsa_tab, ucb_tab], bins = nbr_eq, color = ['yellow', 'blue'],
            edgecolor = 'red', hatch = '/', label = ['IRSA', 'UCB1'],
            histtype = 'bar')
    plt.ylabel('gain')
    plt.xlabel('nombre d équipements')
    plt.title('Comparaison de l algorithem IRSA et UCB1')
    plt.legend()
    plt.show() 

if __name__ == "__main__":
    random.seed()

    # Input for equipment count
    equipments_count = -1
    while equipments_count < 10 or equipments_count > 20:
        try:
            equipments_count = input("Enter how many equipements are there (default = 10): ")
            if not equipments_count:
                equipments_count = 10
            else:
                equipments_count = int(equipments_count)
        except ValueError:
            print("Error: must be an integer! (10 <= number <= 20)")
        if equipments_count < 10 or equipments_count > 20:
            print("Warning: must be a number between 10 and 20")

    # Input for how many packets will be sent by equipment
    packets_count = -1
    while packets_count < 0:
        try:
            packets_count = int(input("Enter the number of packets each equipment will send: "))
        except ValueError:
            print("Error: must be an integer! (> 0)")

    # Create the Base Station
    bs = BaseStation(packets_count * equipments_count)

    avg_gain_irsa = []
    best_strategies_ucb = []
    strategies_irsa = []
    strategies_irsa_gain = []
    lambdas = [x/10 for x in range(1, 50, 2)]

    # Create a list of equipments
    equipments = []
    for i in range(equipments_count):
        e = Equipment(packets_count=packets_count, frame=Frame(index=i))
        equipments.append(e)
            
    bs.set_equipments(equipments)

    for lmbd in lambdas:
        # Testing IRSA for strategy 3
        strategy = random.randint(2, 4)
        for e in equipments:
            e.send_packets(lmbd, strategy)

        # Collision Detection
        collision_table = bs.detect_collisions()

        # Calculating average rewards
        avg_e = []
        for e in equipments:
            avg = sum(e.gain_tab)/len(e.gain_tab)
            avg_e.append(avg)
        avg_gain_irsa.append(sum(avg_e) / len(avg_e))

        gn = max(avg_gain_irsa)
        #stock les gains pour chaque stratégie dans strategies_irsa
        strategies_irsa_gain.append(gn)
        strategies_irsa.append(strategy)

        # Clearing Base Station for UCB Testing
        bs.clear()

        # Testing UCB for all strategies
        best_strategy = None
        best_ucb = -1
        for strategy in range(2, 4):
            for e in equipments:
                e.rand_dist(e.frame, strategy)

            # Collision Detection
            collision_table = bs.detect_collisions()

            # Running UCB1
            ucb = UCB1(equipments)
            if ucb > best_ucb:
                best_ucb = ucb
                best_strategy = strategy
                print(best_strategy)
        best_strategies_ucb.append(best_strategy)
        
        # Clearing Base Station
        bs.clear()

    # TODO Drawing plots of performance

    ## GENERAL INFORMATIONS
    # the packets arrives following Poisson using parameter LAMBDA
    # the equipment chooses randomly k SLOTs from the 10 SLOTs
    #   k : random between 2 and 4

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

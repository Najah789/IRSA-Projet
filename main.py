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
import numpy as np

import random
import math


# UCB1 
def ucb1(equipments:list):
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

def graph_plot(lambdas:list, tab2:list, l:str):
    x = np.array(lambdas)
    y = np.array(tab2)

    plt.xlim([0, 5])
    plt.xticks(np.arange(0, 5, 0.2))
    plt.xlabel("Lambdas")
    plt.ylabel("Stratégies")

    plt.yticks([2, 3, 4])

    plt.plot(x, y, label=l)
    plt.title(f"Meilleure stratégie pour chaque valeur de λ pour {l}")
    plt.legend()
    plt.grid()
    plt.show()

def graph_plot_2(lambdas:list, tab1:list, tab2:list, l:str, l2:str):
    x = np.array(lambdas)
    y = np.array(tab1)
    y2 = np.array(tab2)

    plt.xlim([0, 5])
    plt.xticks(np.arange(0, 5, 0.2))
    plt.xlabel("Lambdas")
    plt.ylabel("Stratégies")

    plt.yticks([2, 3, 4])

    plt.plot(x, y, label=l)
    plt.plot(x, y2, label=l2)
    plt.title(f"Meilleure stratégie pour chaque valeur de λ")
    plt.legend()
    plt.grid()
    plt.show()


def graph_plot_hist(tab1:list, tab2:list, lambdas:list):

    # version 2

    x = np.arange(25)
    width = 0.4
    fig, ax = plt.subplots()
    ax.bar(x - width/2, tab1, width, label='IRSA')
    ax.bar(x + width/2, tab2, width, label='UCB1')

    ax.set_ylabel('Gains')
    ax.set_xlabel('Lambdas')
    ax.set_title('Comparaison de l\'algorithme IRSA et UCB1')
    ax.set_xticks(x)
    ax.set_xticklabels(lambdas)
    ax.legend()

    fig.tight_layout()
    
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
    avg_gain_ucb =[]
    best_strategies_ucb = []
    best_strategies_ucb_gain = []
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
        for strategy in range(2, 5):
            for e in equipments:
                e.rand_dist(strategy)

            # Collision Detection
            collision_table = bs.detect_collisions()

            # Running UCB1
            ucb = ucb1(equipments)
            if ucb > best_ucb:
                best_ucb = ucb
                best_strategy = strategy
            
        # On calcule le gain pour la stratégie choisi par UCB1
        for e in equipments:
            e.rand_dist(best_strategy)

        # Collision Detection
        collision_table = bs.detect_collisions()

        # Calculating average rewards
        avg_e = []
        for e in equipments:
            avg_e.append(sum(e.gain_tab) / len(e.gain_tab))
        avg_gain_ucb.append(sum(avg_e) / len(avg_e))

        gn = max(avg_gain_ucb)     
        best_strategies_ucb_gain.append(gn)
        best_strategies_ucb.append(best_strategy)
        
        # Clearing Base Station
        bs.clear()

    graph_plot(lambdas, strategies_irsa, 'IRSA')
    graph_plot(lambdas, best_strategies_ucb, 'UCB')
    graph_plot_2(lambdas, strategies_irsa, best_strategies_ucb, 'IRSA', 'UCB')
    graph_plot_hist(strategies_irsa_gain, best_strategies_ucb_gain, lambdas)

    """ EXAMPLE

        S represents a slot
        X represents a frame (trame en français :p)
        C represents a collision

        |------------|S (1)|S (2)|S (3)|S (4)|S (5)|S (6)|S (7)|S (8)|S (9)|S(10)|
        |EQUIPMENT 1 |--X--|-----|--X--|-----|--X--|-----|-----|--X--|-----|--X--| <- Frame 1
        |EQUIPMENT 2 |--X--|-----|-----|--X--|-----|-----|-----|-----|--X--|-----| <- Frame 2
        |EQUIPMENT 3 |-----|--X--|-----|-----|--X--|-----|--X--|-----|--X--|-----| <- Frame 3
        |------------|-----------------------------------------------------------|
        |BROADCAST   |--C--|--X--|--X--|--X--|--C--|-----|--X--|--X--|--C--|--X--| <- Frame of BS 
        |------------|-----------------------------------------------------------|
    """

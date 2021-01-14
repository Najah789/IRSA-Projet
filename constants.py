"""
    Constant definitions
"""

MAX_NUM_OF_SLOTS = 10

## Inputs
    # lambda (input)
    # k (number of repetitions) (input)

## Variables
    # buffer of packets sent
    # send a packet every tick > tick calculated using "loi de Poisson"

## Classes
    # packet
        # "character"

    # machines
        # index
        # paquets (list of packet)

    # slot
        # index
        # packet
        # chosen (bool)

    # base_station
        # ack (0.9, 0.4, 0.1)

    # frame 'trame'
        # slots (list of slot)
        # collisions (list of boolean)

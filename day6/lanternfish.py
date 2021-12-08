import sys
from collections import defaultdict
from pprint import pprint

__doc__ = """
Lanternfish (AoC 2021, day 6)

  lanternfish.py input_file sim_days

sim_days is an integer, specifying the number of cycles for the simulation
"""

def usage():
    print(__doc__)

def read_input(stream):
    return list(map(int, stream.readline().strip().split(',')))

def simulate(model):
    """
    Simulate one day
    """
    result = defaultdict(int)
    for days_left, num_fish in sorted(model.items(), reverse=True):
        if days_left == 0:
            result[6] += num_fish
            result[8] = num_fish
        else:
            result[days_left-1] = num_fish
    return result

def main(data, days):
    model = defaultdict(int)

    for dl in data:
        model[dl] += 1

    for _ in range(days):
        model = simulate(model)
    print(sum(model.values()))


if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as stream:
            main(read_input(stream), int(sys.argv[2]))
    except IndexError:
        usage()

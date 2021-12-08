import sys
import math
from collections import defaultdict
from pprint import pprint

def read_input(stream):
    for line in stream:
        digits, output = map(lambda x: tuple(x.strip().split()), line.split('|'))
        yield digits, output

def find_with_length(lst, ln):
    for n, elem in enumerate(lst):
        if len(elem) == ln:
            return n

    raise IndexError(f"Not such element with length {ln}")

def translate_digits(digits):
    length_map = defaultdict(set)
    for d in digits:
        length_map[len(d)].add(d)
    rmapping = {
            '1': frozenset(length_map[2].pop()),
            '7': frozenset(length_map[3].pop()),
            '4': frozenset(length_map[4].pop()),
            '8': frozenset(length_map[7].pop())
            }

    one  = rmapping['1']
    four = rmapping['4']

    sixes = [set(s) for s in length_map[6]]
    fives = [set(f) for f in length_map[5]]

    rmapping['6'] = frozenset(sixes.pop(find_with_length([s - one for s in sixes], 5)))
    rmapping['9'] = frozenset(sixes.pop(find_with_length([s - four for s in sixes], 2)))
    rmapping['0'] = frozenset(sixes.pop())
    rmapping['3'] = frozenset(fives.pop(find_with_length([f - one for f in fives], 3)))
    rmapping['5'] = frozenset(fives.pop(find_with_length([f - rmapping['9'] for f in fives], 0)))
    rmapping['2'] = frozenset(fives.pop())

    return dict((v, k) for (k, v) in rmapping.items())

def main(data):
    unique_l = {2, 3, 4, 7}
    total_uniq = 0
    total = 0
    for digits, output in data:
        mapping = translate_digits(digits)
        total_uniq += sum(len(o) in unique_l for o in output)
        total += int(''.join(mapping[frozenset(o)] for o in output))
    print('Part 1:', total_uniq)
    print('Part 2:', total)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

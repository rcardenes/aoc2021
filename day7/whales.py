import sys
import math
from collections import defaultdict
from pprint import pprint
from functools import reduce

def read_input(stream):
    return list(map(int, stream.readline().strip().split(',')))

def median(data):
    ldata = len(data)
    hl = (ldata // 2)
    if ldata % 2 == 0:
        return (data[hl-1] + data[hl]) // 2
    else:
        return data[hl]

def mean(data):
    return sum(data) / len(data)

def sum_first_n(n):
    return n*(n+1) // 2

def main(data):
    sdata = sorted(data)
    md = median(sdata)
    mn = mean(sdata)
    print('Part 1:', sum(abs(y - md) for y in data))
    print('Part 2:', min(*[sum(sum_first_n(abs(y - m)) for y in data) for m in (math.floor(mn), math.ceil(mn))]))

if __name__ == '__main__':
    main(read_input(open(sys.argv[1])))

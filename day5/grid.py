import sys
from collections import defaultdict

def to_point(string):
    return tuple(int(x) for x in string.split(','))

def read_input(stream):
    for line in stream:
        a, b = line.strip().split(' -> ')
        x1, y1 = to_point(a)
        x2, y2 = to_point(b)

        if (x1 == x2 and y2 < y1) or (x2 < x1):
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        yield x1, y1, x2, y2

def generate_segment(x1, y1, x2, y2, with_diagonals=False):
    diagonal = x1 != x2 and y1 != y2
    if not with_diagonals and diagonal:
        return

    yield x1, y1

    if (x1, y1) != (x2, y2):
        if diagonal:
            delta = (1, (1 if y1 < y2 else -1))
        else:
            delta = (0, 1) if x1 == x2 else (1, 0)
        while (x1, y1) != (x2, y2):
            x1, y1 = x1 + delta[0], y1 + delta[1]
            yield x1, y1

def main(data_input):
    grid_a = defaultdict(int)
    grid_b = defaultdict(int)
    for x1, y1, x2, y2 in data_input:
        for point in generate_segment(x1, y1, x2, y2):
            grid_a[point] += 1
        for point in generate_segment(x1, y1, x2, y2, with_diagonals=True):
            grid_b[point] += 1
    print("Part 1:", len(tuple(x for x in grid_a.values() if x > 1)))
    print("Part 2:", len(tuple(x for x in grid_b.values() if x > 1)))

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))


import sys
import numpy as np
from collections import defaultdict
import pdb

def fold_up(paper, line):
    upper, lower = paper[:line], np.flipud(paper[line+1:])
    up_h, low_h = upper.shape[0], lower.shape[0]
    if low_h > up_h:
        lower, upper = upper, lower
        up_h, low_h = low_h, up_h

    overlapping = up_h - low_h
    upper[overlapping:] = np.logical_or(upper[overlapping:], lower)
    return upper

def fold_left(paper, line):
    left, right = paper[:,:line], np.fliplr(paper[:,line+1:])
    left_h, right_h = left.shape[0], right.shape[0]
    if right_h > left_h:
        right, left = left, right
        left_h, right_h = right_h, left_h

    overlapping = left_h - right_h
    left[:,overlapping:] = np.logical_or(left[:,overlapping:], right)
    return left

def count_dots(paper):
    return len(np.where(paper)[0])

def printout(paper):
    for row in paper:
        print(''.join('x' if cell else ' ' for cell in row))

def main(data):
    coords, folds = data
    max_x = max(tuple(x for (x, y) in coords))
    max_y = max(tuple(y for (x, y) in coords))
    paper = np.zeros((max_y+1, max_x+1), dtype=bool)
    for x, y in coords:
        paper[y,x] = True

    after_first = None
    for axis, coord in folds:
        if axis == 'y':
            paper = fold_up(paper, coord)
        else:
            paper = fold_left(paper, coord)
        if after_first is None:
            after_first = count_dots(paper)

    print("Part 1:", after_first)
    printout(paper)

def read_input(stream):
    reading_coords = True
    coords = []
    folds = []
    max_x, max_y = 0, 0
    for line in stream:
        if not line.strip():
            reading_coords = False
        elif reading_coords:
            newest = tuple(map(int, line.strip().split(',')))
            max_x = max(max_x, newest[0])
            max_y = max(max_y, newest[1])
            coords.append(newest)
        else:
            axis, coord = line.strip().split()[-1].split('=')
            folds.append((axis, int(coord)))

    return coords, folds

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

import sys
import numpy as np
import pdb

def is_local_minimum_1d(arr):
    if len(arr) == 1:
        return np.array([True])

    ret = np.empty(arr.shape, dtype=bool)
    ret[0] = arr[0] < arr[1]
    ret[-1] = arr[-1] < arr[-2]
    if len(ret) > 2:
        ret[1:-1] = np.array([arr[i-1] > arr[i] and arr[i] < arr[i+1] for i in range(1, len(ret)-1)])

    return ret

def basin_size(data, coords):
    in_basin = set()
    search = {coords}
    diffs = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    maxy, maxx = data.shape
    while search:
        current = search.pop()
        if (-1 < current[0] < maxy) and (-1 < current[1] < maxx) and data[current] < 9:
            in_basin.add(current)
            search |= set((current[0]+dfy, current[1]+dfx) for (dfy, dfx) in diffs) - in_basin

    return len(in_basin)

def main(data):
    minima = np.logical_and(np.apply_along_axis(is_local_minimum_1d, 1, data),
                            np.apply_along_axis(is_local_minimum_1d, 0, data))
    print('Part 1:', (data[minima]+1).sum())

    all_coords = np.where(minima)
    basin_sizes = sorted(basin_size(data, coords) for coords in zip(*all_coords))
    print('Part 2:', np.array(basin_sizes[-3:], dtype=int).prod())

def read_input(stream):
    raw_map = [tuple(map(int, line.strip())) for line in stream]
    return np.array(raw_map, dtype=int)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

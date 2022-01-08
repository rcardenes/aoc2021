import sys
import numpy as np
import time

UNDEFINED = (-1, -1)

def initialize_maps(shape):
    return (
        np.ones(shape) * np.inf,
        np.empty(shape, dtype=object),
        np.zeros(shape, dtype=bool)
        )

def find_unvisited(current, vis_map):
    mr, mc = vis_map.shape
    cr, cc = current
    for row, col in ((cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)):
        if (-1 < row < mr) and (-1 < col < mc) and not vis_map[row, col]:
            yield (row, col)

def get_next_node(candidates, distances):
    _, coords = min(((distances[cnd], cnd) for cnd in candidates))
    return coords

def calc_path(data, start, goal):
    distances, previous, visited = initialize_maps(data.shape)
    distances[start] = 0

    next_node = start
    may_visit_next = set()

    while next_node != goal:
        visited[next_node] = True
        d_current = distances[next_node]
        for candidate in find_unvisited(next_node, visited):
            dist_from_here = d_current + data[candidate]
            if dist_from_here < distances[candidate]:
                distances[candidate] = dist_from_here
                previous[candidate] = next_node
                may_visit_next.add(candidate)

        next_node = get_next_node(may_visit_next, distances)
        may_visit_next.remove(next_node)

    path = []
    next_in_path = goal
    while next_in_path != start:
        path.append(next_in_path)
        next_in_path = previous[next_in_path]

    return path

def total_risk(path, risk_data):
    return sum(risk_data[coords] for coords in path)

def generate_full_map(risk_map):
    tile = risk_map[:,:] - 1
    full_row = np.hstack([(tile+k) % 9 for k in range(5)])
    return np.vstack([(full_row+k) % 9 for k in range(5)]) + 1

def main(data):
    rows, cols = data.shape
    print("Part 1:", total_risk(calc_path(data, start=(0, 0), goal=(rows-1, cols-1)), data))

    full_map = generate_full_map(data)
    rows, cols = full_map.shape
    print("Part 2:", total_risk(calc_path(full_map, start=(0, 0), goal=(rows-1, cols-1)), full_map))


def read_input(stream):
    cave_map = []
    for line in stream:
        cave_map.append(list(map(int, line.strip())))
    return np.array(cave_map, dtype=int)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

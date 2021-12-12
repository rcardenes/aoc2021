import sys
from collections import defaultdict

def walk(the_map, current, visited, path, visited_twice, can_visit_twice=False):
    if current == 'end':
        yield path
    else:
        for candidate in the_map[current]:
            lower_and_visited = candidate.islower() and candidate in visited
            if candidate == 'start':
                continue
            elif lower_and_visited:
                if not can_visit_twice or visited_twice:
                    continue

            yield from walk(the_map, candidate, visited | {candidate}, path + [candidate], visited_twice | lower_and_visited, can_visit_twice)

def main(data):
    the_map = defaultdict(set)
    for edge in data:
        a, b = edge.split('-')
        the_map[a].add(b)
        the_map[b].add(a)

    print('Part 1:', len(list(walk(the_map, 'start', {'start'}, ['start'], False))))
    print('Part 2:', len(list(walk(the_map, 'start', {'start'}, ['start'], False, True))))

def read_input(stream):
    for line in stream:
        yield line.strip()

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

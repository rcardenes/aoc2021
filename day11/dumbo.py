import sys
import numpy as np

def simulate_step(data):
    sim = data.copy()
    flashed = np.zeros(data.shape, dtype=bool)
    sim += 1
    while True:
        new_flashes = np.logical_and(sim > 9, np.logical_not(flashed))
        if new_flashes.any():
            flashed = np.logical_or(flashed, new_flashes)
            for (y, x) in zip(*np.where(new_flashes)):
                sim[max(y-1, 0):y+2, max(x-1, 0):x+2] += 1
        else:
            break

    sim[sim > 9] = 0

    return sim, len(sim[flashed])

def main(data):
    nsteps = 0
    total_flashes = 0
    while True:
        data, nflashed = simulate_step(data.copy())
        if nsteps < 100:
            total_flashes += nflashed
        nsteps += 1
        if not data.any():
            break

    print('Part 1:', total_flashes)
    print('Part 2:', nsteps)

def read_input(stream):
    return np.array([list(map(int, line.strip())) for line in stream], dtype=int)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

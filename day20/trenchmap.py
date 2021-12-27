import sys
import numpy as np
from functools import partial

class Image:
    def __init__(self, data):
        if isinstance(data, np.ndarray):
            self.data = data
        else:
            self.data = np.array([[('1' if c=='#' else '0') for c in row] for row in data], dtype=str)

    def __repr__(self):
        return '\n'.join(''.join(('#' if c=='1' else '.') for c in row) for row in self.data)

    def iterate(self, proc_algo, algo, num):
        result = self.data
        bkg_index = None
        while num > 0:
            num = num - 1
            rows, cols = result.shape
            try:
                bkg_value = '1' if algo[bkg_index] == '#' else '0'
            except TypeError:
                bkg_value = '0'
            processing_array = np.full((rows + 4, cols + 4), bkg_value, dtype=str)
            processing_array[2:-2, 2:-2] = result
            result = np.array([proc_algo(algo, processing_array[y-1:y+2, x-1:x+2]) for y in range(1, rows+3) for x in range(1, cols+3)], dtype=str).reshape((rows+2, cols+2))
            bkg_index = to_dec(processing_array[0:3,0:3])

        return Image(result)

    def count_lit(self):
        return len(self.data[self.data == '1'])

def to_dec(kernel):
    return int(''.join(kernel.ravel()), 2)

def process_algorithm(algo, kernel):
    return '1' if algo[to_dec(kernel)] == '#' else 0

def print_both(arr1, arr2):
    for line1, line2 in zip(str(Image(arr1)).split('\n'), str(Image(arr2)).split('\n')):
        print(f"{line1} {line2}")

def main(data):
    algorithm, image = data

    iterated = image.iterate(process_algorithm, algorithm, 2)
    print("Part 1:", iterated.count_lit())

    iterated = image.iterate(process_algorithm, algorithm, 50)
    print("Part 2:", iterated.count_lit())

def read_input(stream):
    alg = stream.readline().strip()
    stream.readline()
    image = Image([line.strip() for line in stream])

    return alg, image

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

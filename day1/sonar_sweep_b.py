import sys

def read_input(stream):
    return [int(x) for x in stream]

def main(data):
    windowed = [a + b + c for (a, b, c) in zip(data[:-2], data[1:-1], data[2:])]
    print(sum((x1 - x2) > 0 for (x1, x2) in zip(windowed[1:], windowed[:-1])))

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

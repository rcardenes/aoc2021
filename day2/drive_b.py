import sys

def read_input(stream):
    for line in stream:
        instr, offs = line.strip().split()
        yield instr, int(offs)

def main(data):
    x = 0
    depth = 0
    aim = 0
    for instr, offs in data:
        if instr == 'forward':
            x += offs
            depth += aim * offs
        elif instr == 'up':
            aim -= offs
        elif instr == 'down':
            aim += offs
        else:
            print(f'Unknown instruction {instr}')

    print(f'{x} * {depth} = {x * depth}')

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

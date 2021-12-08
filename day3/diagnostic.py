import sys

def read_input(stream):
    return [tuple(int(x) for x in line.strip().split()[0]) for line in stream]

most_common = lambda x, half: 1 if (x >= half) else 0
least_common = lambda x, half: 0 if (x >= half) else 1

def stats(numbers, bits, fn):
    sums = [0] * bits

    for n, bits in enumerate(numbers, 1):
        sums = [a + b for (a, b) in zip(sums, bits)]

    total = n
    half = total / 2

    return tuple(fn(k, half) for k in sums)

def filter_by(data, bits, fn):
    datac = data[:]
    current = 0
    while len(datac) > 1:
        mc = stats(datac, bits, fn)
        token = mc[current]
        datac = tuple(x for x in datac if x[current] == token)
        current += 1

    return datac[0]

def calc_epsilon(gamma, nbits):
    return (2**nbits - 1) - gamma

def to_dec(bits):
    return int(''.join(str(b) for b in bits), base=2)

def main(data):
    nbits = len(data[0])
    mc = stats(data, nbits, most_common)
    gamma = to_dec(mc)
    epsilon = calc_epsilon(gamma, nbits)
    ox_gen = to_dec(filter_by(data, nbits, most_common))
    co2_scrub = to_dec(filter_by(data, nbits, least_common))

    print("gamma * epsilon: ", gamma * epsilon)
    print("O2 gen * CO2 scr:", ox_gen * co2_scrub)

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

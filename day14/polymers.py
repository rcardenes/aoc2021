import sys
from collections import Counter, defaultdict
from operator import itemgetter

def expand(template, rules, steps):
    pairs = defaultdict(int)
    cnt = Counter(template)

    for a, b in zip(template[:-1], template[1:]):
        pairs[a+b] += 1

    while steps:
        new_pairs = defaultdict(int)
        for pair, count in pairs.items():
            a, b = pair
            new_char = rules[pair]
            new_pairs[a + new_char] += count
            new_pairs[new_char + b] += count
            cnt[new_char] += count
        steps -= 1
        pairs = new_pairs

    return cnt

def solve_and_print(template, rules, steps):
    counter = expand(template, rules, steps)
    srtd = sorted(counter.items(), key=itemgetter(1))
    print(f"After {steps} steps, the difference is: {srtd[-1][1] - srtd[0][1]}")

def main(data):
    template, rules = data
    solve_and_print(template, rules, 10)
    solve_and_print(template, rules, 40)

def read_input(stream):
    template = stream.readline().strip()
    stream.readline()
    rules = dict(tuple(line.strip().split(' -> ')) for line in stream)
    return template, rules

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

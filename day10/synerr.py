import sys

class MySyntaxError(Exception):
    ...

def recognize_line(line):
    closing_pairs = {
            ')': '(',
            ']': '[',
            '}': '{',
            '>': '<'
            }
    opening_pairs = dict((v,k) for (k,v) in closing_pairs.items())

    stack = []
    for ch in line:
        if ch not in closing_pairs:
            stack.append(ch)
        elif stack.pop() != closing_pairs[ch]:
            raise MySyntaxError(ch)

    while stack:
        yield opening_pairs[stack.pop()]

    return stack

def main(data):
    ILLEGAL_SCORE = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
            }
    CLOSING_SCORE = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
            }

    corrupted_score = 0
    completion_scores = []
    for line in data:
        local_score = 0
        try:
            for ch in recognize_line(line):
                local_score = local_score * 5 + CLOSING_SCORE[ch]
            completion_scores.append(local_score)
        except MySyntaxError as mse:
            corrupted_score += ILLEGAL_SCORE[mse.args[0]]

    print('Part 1:', corrupted_score)
    print('Part 2:', sorted(completion_scores)[len(completion_scores) // 2])

def read_input(stream):
    for line in stream:
        yield line.strip()

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

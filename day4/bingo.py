import sys

class Board:
    def __init__(self, numbers):
        self.numbers = set(numbers)
        self.rows = tuple(numbers[k:k+5] for k in range(0, 25, 5))
        self.cols = tuple(numbers[k::5] for k in range(5))
        self.announced = set()

    def __repr__(self):
        return '\n'.join(' '.join(str(n) for n in row) for row in self.rows)

    def is_winner(self):
        for subset in self.rows + self.cols:
            if set(subset).issubset(self.announced):
                return True

    def unmarked(self):
        return self.numbers - self.announced

    def number_announced(self, n):
        self.announced.add(n)

def read_input(stream):
    yield [int(x) for x in stream.readline().strip().split(',')]

    while True:
        # Discard blank line
        blank = stream.readline()
        if not blank:
            break
        board_numbers = [int(x) for x in (
                stream.readline() +
                stream.readline() +
                stream.readline() +
                stream.readline() +
                stream.readline()
                ).strip().split()]
        yield Board(board_numbers)

def print_sum(board, wnum):
    print(sum(board.unmarked()) * wnum)

def main(data_input):
    drawn = next(data_input)
    boards = set(data_input)

    winners = []

    for n in drawn:
        for b in boards.copy():
            b.number_announced(n)
            if b.is_winner():
                winners.append((b, n))
                boards.remove(b)
        if not boards:
            break

    print_sum(*winners[0])
    print_sum(*winners[-1])

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

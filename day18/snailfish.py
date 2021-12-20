import sys
import json
from math import ceil, floor
from copy import deepcopy
from itertools import permutations

class Explosion(Exception):
    ...

class Split(Exception):
    ...

class RegularNumber:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def magnitude(self):
        return self.value

    def explode(self, level):
        return None

    def split(self):
        if self.value > 9:
            raise Split(Pair(RegularNumber(int(floor(self.value / 2))),
                             RegularNumber(int(ceil(self.value / 2)))))

    def addleft(self, number):
        self.value = self.value + number.magnitude()

    def addright(self, number):
        self.value = self.value + number.magnitude()

class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'[{self.left}, {self.right}]'

    def __add__(self, other):
        return Pair(deepcopy(self), deepcopy(other)).reduce()

    def __radd__(self, other):
        if other is None:
            return deepcopy(self)

    def explodable(self):
        return isinstance(self.left, RegularNumber) and isinstance(self.right, RegularNumber)

    def parts(self):
        return self.left, self.right


    def magnitude(self):
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    def explode(self, level=1):
        if level > 4:
            if self.explodable():
                raise Explosion({'left': self.left, 'right':self.right})

        try:
            actions = self.left.explode(level + 1)
        except Explosion as exp:
            actions = exp.args[0]
            self.left = RegularNumber(0)

        if actions is True:
            return True
        elif isinstance(actions, dict):
            try:
                self.right.addleft(actions.pop('right'))
            except KeyError:
                ...
            return actions or True

        try:
            actions = self.right.explode(level + 1)
        except Explosion as exp:
            actions = exp.args[0]
            self.right = RegularNumber(0)

        if actions is True:
            return True
        elif isinstance(actions, dict):
            try:
                self.left.addright(actions.pop('left'))
            except KeyError:
                ...
            return actions or True

    def split(self):
        try:
            if not self.left.split():
                try:
                    return self.right.split()
                except Split as spl:
                    self.right = spl.args[0]
                    return True
            else:
                return True
        except Split as spl:
            self.left = spl.args[0]
            return True

    def addleft(self, number):
        self.left.addleft(number)

    def addright(self, number):
        self.right.addright(number)

    def reduce(self):
        modified = True
        while modified:
            modified = self.explode() or self.split()
        return self

def frominput(inp):
    if isinstance(inp, int):
        return RegularNumber(inp)
    else:
        return Pair(frominput(inp[0]), frominput(inp[1]))

def main(data):
    numbers = [frominput(sfn) for sfn in data]

    print("Part 1:", sum(numbers, None).magnitude())

    print("Part 2:", max((p1 + p2).magnitude() for (p1, p2) in permutations(numbers, 2)))

def read_input(stream):
    for line in stream:
        yield json.loads(line.strip())

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        main(read_input(stream))

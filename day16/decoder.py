import sys
import operator
from functools import reduce
from math import log2

class InputStream:
    def __init__(self, bits):
        self.bits = bits

    def eof(self):
        return len(self.bits) < 8

    def get_next(self, nbits):
        if not self.bits:
            raise StopIteration
        ret, self.bits = self.bits[:nbits], self.bits[nbits:]
        return ret

class Literal:
    def __init__(self, version):
        self.version = version
        self.bits = ''

    def __repr__(self):
        return str(self.value())

    def add(self, bits):
        self.bits = self.bits + bits

    def version_sum(self):
        return self.version

    def value(self):
        return int(self.bits, 2)

class Operator:
    def __init__(self, version, op_type):
        self.version = version
        self.op_type = op_type
        self.children = []

    def __repr__(self):
        return f"<Op {self.children}>"

    def add(self, child):
        self.children.append(child)

    def version_sum(self):
        return self.version + sum(ch.version_sum() for ch in self.children)

    def value(self):
        ch_values = tuple(ch.value() for ch in self.children)
        if self.op_type == 0:
            return sum(ch_values)
        elif self.op_type == 1:
            return reduce(operator.mul, ch_values, 1)
        elif self.op_type == 2:
            return min(ch_values)
        elif self.op_type == 3:
            return max(ch_values)
        elif self.op_type == 5:
            return int(ch_values[0] > ch_values[1])
        elif self.op_type == 6:
            return int(ch_values[0] < ch_values[1])
        elif self.op_type == 7:
            return int(ch_values[0] == ch_values[1])

def decode_packet(data):
    header = data.get_next(6)
    version = int(header[:3], 2)
    packet_type = int(header[3:], 2)
    if packet_type == 4:
        packet = Literal(version)
        while True:
            block = data.get_next(5)
            packet.add(block[1:])
            if block[0] == '0':
                break
    else:
        # Operator
        packet = Operator(version, packet_type)
        length_type_id = data.get_next(1)
        if length_type_id == '0':
            payload_length = int(data.get_next(15), 2)
            substream = InputStream(data.get_next(payload_length))
            while not substream.eof():
                packet.add(decode_packet(substream))
        else:
            packets_left = int(data.get_next(11), 2)
            while packets_left:
                packet.add(decode_packet(data))
                packets_left -= 1

    return packet

def main(data_stream):
    packet = decode_packet(data_stream)
    print("Part 1:", packet.version_sum())
    print("Part 2:", packet.value())

def get_input_stream(raw_data):
    hex_num = raw_data
    first = int(hex_num[:2], 16)
    padding = "0" * (7 - int(log2(first)))
    bin_rep = padding + bin(int(hex_num, 16))[2:]
    return InputStream(bin_rep)

def read_input(stream):
    return get_input_stream(stream.readline().strip())

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as stream:
            main(read_input(stream))
    except FileNotFoundError:
        main(get_input_stream(sys.argv[1]))

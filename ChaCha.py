from Block import Block, Long


class ChaChaStream(object):
    def __init__(self, key: bytes, nonce: bytes):
        self.key = key
        self.nonce = nonce
        self.counter = 0
        self.stream = 0
        self.block = None

    def set_key(self, key: bytes):
        self.counter = 0
        self.key = key

    def set_nonce(self, nonce: bytes):
        self.counter = 0
        self.nonce = nonce

    def generate(self):
        if self.counter >= 2**32:
            raise OverflowError("The counter has overflowed, need a new Nonce or Key")

        self.block = Block(self.key, self.counter.to_bytes(4, 'big'), self.nonce)
        copy = self.block.copy()
        for _ in range(10):
            self.double_round()

        self.counter = self.counter+1
        self.block = self.block+copy

        data = int(self.block)
        stream = 0

        for _ in range(data.bit_length()):
            stream = (stream << 1) | (data & 1)
            data = data >> 1

        self.stream = self.stream | (stream << self.stream.bit_length())

    def read_bit(self):
        if self.stream.bit_length() == 0:
            self.generate()
        out = self.stream & 1
        self.stream = self.stream >> 1
        return out

    def read_bits(self, bit_count):
        out = 0
        for _ in range(bit_count):
            out = (out << 1) | self.read_bit()
        return out

    def read_bytes(self, byte_count):
        out = b''
        for _ in range(byte_count):
            out = out+int.to_bytes(self.read_bits(8), 1, 'big')
        return out

    def double_round(self):
        self.quarter_round(0, 4,  8, 12)  # 1st column
        self.quarter_round(1, 5,  9, 13)  # 2nd column
        self.quarter_round(2, 6, 10, 14)  # 3rd column
        self.quarter_round(3, 7, 11, 15)  # 4th column
        # Even round
        self.quarter_round(0, 5, 10, 15)  # diagonal 1 (main diagonal)
        self.quarter_round(1, 6, 11, 12)  # diagonal 2
        self.quarter_round(2, 7,  8, 13)  # diagonal 3
        self.quarter_round(3, 4,  9, 14)  # diagonal 4

    def quarter_round(self, *indecies):
        a, b, c, d = [self.block[index] for index in indecies]

        a = a + b
        d = d ^ a
        d.lrotate(16)

        c = c + d
        b = b ^ c
        b.lrotate(12)

        a = a + b
        d = d ^ a
        d.lrotate(8)

        c = c + d
        b = b ^ c
        b.lrotate(7)

        for index, val in zip(indecies, [a, b, c, d]):
            self.block[index] = val

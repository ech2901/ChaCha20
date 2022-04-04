class Long(object):
    def __init__(self, val):
        if type(val) == int:
            self.data = (val & 0xff_ff_ff_ff).to_bytes(4, 'little')
        elif type(val) == bytes:
            self.data = val

    def copy(self):
        return Long(self.data)

    def __int__(self):
        return int.from_bytes(self.data, 'little')

    def __bytes__(self):
        return self.data

    def __repr__(self):
        return self.data.hex()

    def __str__(self):
        return self.data.hex()

    def __add__(self, other):
        return Long(int(self) + int(other))

    def __xor__(self, other):
        return Long(int(self) ^ int(other))

    def lrotate(self, bits):
        new_tail = int(self) >> (32-bits)
        new_head = int(self) << bits
        new_int = (new_head | new_tail) & 0xff_ff_ff_ff
        self.data = new_int.to_bytes(4, 'little')


class Block(object):
    def __init__(self, key: bytes, counter: bytes, nonce: bytes):
        assert len(key) == 32, 'Key size must be 256 bits.'
        assert len(counter) == 4, 'Counter must be 32 bits.'
        assert len(nonce) == 12, 'Nonce must be 96 bits.'

        temp_data = b'expand 32-byte k'+key+counter+nonce
        self.data = [Long(temp_data[i*4:(i*4)+4]) for i in range(16)]

    def copy(self):
        other = Block(bytes(32), bytes(4), bytes(12))
        other.data = self.data.copy()
        return other

    def __getitem__(self, index) -> Long:
        return self.data[index]

    def __setitem__(self, index, value: Long) -> None:
        self.data[index] = value

    def __repr__(self) -> str:
        out = ''.join(map(str, self.data))
        return out

    def __add__(self, other):
        out = Block(bytes(32), bytes(4), bytes(12))
        for index in range(16):
            out[index] = self[index] + other[index]

        return out

    def __int__(self):
        return int(repr(self), 16)



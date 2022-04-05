# ChaCha
ChaCha20 stream cipher implementation
To install the current release:
```
$ pip install ChaCha20
```

How to use the ChaCha20 stream cipher:
```
from ChaCha20 import ChaChaStream
key = bytes(32)  # key can be any byte object with 32 bytes of data
nonce = bytes(12)  # nonce can be any byte object with 12 bytes of data

stream = ChaChaStream(key, nonce)

# pulls 1 bit from the stream, returns an integer
bit = stream.read_bit()

# pulls 200 bits from the stream, returns an integer
bits = stream.read_bits(200)

# pulls 12 bytes from the stream, returns a bytes object
byte_data = stream.read_bytes(12)
```

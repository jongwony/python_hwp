import struct
from io import BytesIO

from .ctrl import char_ctrl

WCHAR = 2


class MainText:
    def __init__(self, stream):
        self.stream = BytesIO(stream)
        self.ctrl = None

    def __iter__(self):
        return self

    def __next__(self):
        def condition(x):
            return 0 < x <= 0x1f

        self.info = b''
        self.data = b''

        b = self.stream.read(WCHAR)
        while b:
            char = struct.unpack('<H', b)[0]
            if condition(char):
                self.ctrl = char
                if char not in char_ctrl:
                    i = self.stream.read(WCHAR)
                    while b != i:
                        self.info += i
                        i = self.stream.read(WCHAR)
                break
            self.data += b
            b = self.stream.read(WCHAR)
        else:
            raise StopIteration

        return self

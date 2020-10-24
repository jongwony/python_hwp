import struct
from io import BytesIO

from .tag_id import is_main
from util.io import parse_header

DWORD = 4


class DataRecord:
    def __init__(self, stream):
        self.stream = BytesIO(stream)

        # header
        self.tag_id = None
        self.level = None
        self.size = None

        self.data = None

    def __repr__(self):
        return f'{self.tag_id} {self.level} {self.size} {self.data}'

    def __iter__(self):
        return self

    def __next__(self):
        b = self.stream.read(DWORD)
        if b == b'':
            raise StopIteration

        d = parse_header(b, is_main)
        if d is None:
            return

        self.tag_id = d['tag_id']
        self.level = d['level']
        self.size = d['size']
        if d['size'] > 0xfff:
            self.size = struct.unpack('<I', self.stream.read(DWORD))[0]
        self.data = self.stream.read(self.size)

        return self


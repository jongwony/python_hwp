from .ctrl import char_ctrl
from util.io import find_pos


class MainText:
    def __init__(self, stream):
        self.stream = stream
        self.info = None
        self.ctrl = None
        self.data = None

    def __iter__(self):
        return self

    def __next__(self):
        def condition(x):
            return 0 <= x <= 0x1f

        if len(self.stream) <= 0:
            raise StopIteration

        pos = find_pos(self.stream, condition)
        if pos == -1:
            self.data = self.stream
            self.stream = b''
            return self.data

        self.ctrl = self.stream[pos]
        if self.ctrl in char_ctrl:
            self.data = self.stream[:pos]
            self.stream = self.stream[pos + 1:]
            return self.data
        else:
            self.data = self.stream[:pos]
            self.info = self.stream[pos + 1:pos + 7]
            self.stream = self.stream[pos + 8:]
            return self.data

UNUSABLE = 0x0
RESERVED = 0x1
DEF_AREA = 0x2
FIELD_START = 0x3
FIELD_END = 0x4
RESERVED = 0x5
RESERVED = 0x6
RESERVED = 0x7
TITLE_MARK = 0x8
TAB = 0x9
LINE_BREAK = 0xa
DRAW = 0xb
RESERVED = 0xc
PARA_BREAK = 0xd
RESERVED = 0xe
HIDE_DESC = 0xf
HEADER_FOOTER = 0x10
FOOTNOTE_ENDNOTE = 0x11
AUTO_NUM = 0x12
RESERVED = 0x13
RESERVED = 0x14
PAGE_CTRL = 0x15
BOOKMARK = 0x16
COMMENT = 0x17
HYPHEN = 0x18
RESERVED = 0x19
RESERVED = 0x1a
RESERVED = 0x1b
RESERVED = 0x1c
RESERVED = 0x1d
BUNDLE = 0x1e
FIXED_WIDTH = 0x1f

char_ctrl = [UNUSABLE, LINE_BREAK, PARA_BREAK, HYPHEN, 25, 26, 27, 28, 29, BUNDLE, FIXED_WIDTH]
inline_ctrl = [FIELD_END, 5, 6, 7, TITLE_MARK, TAB, 19, 20]
extended_ctrl = [1, DEF_AREA, FIELD_START, DRAW, 12, 14, HIDE_DESC, HEADER_FOOTER, FOOTNOTE_ENDNOTE, AUTO_NUM, PAGE_CTRL,
                 BOOKMARK, COMMENT]


class FilterData:
    def __init__(self, stream):
        self.stream = stream
        self.info = None
        self.ctrl = None
        self.data = None

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.stream) <= 0:
            raise StopIteration

        pos = 0
        while pos < len(self.stream):
            if int(self.stream[pos]) <= 0x1f:
                break
            pos += 1
        else:
            # pos = -1
            raise StopIteration

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

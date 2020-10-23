import zlib

from olefile import OleFileIO

from .tag_id import *
from .ctrl import *

HWP_WBITS = -15


class Record:
    def __init__(self, stream):
        tag_idx = stream.find(HWPTAG_PARA_HEADER)
        stream[tag_idx]


def iter_text(stream):
    with OleFileIO(stream) as ole:
        body_text = ['/'.join(ls) for ls in ole.listdir() if 'BodyText' in ls]
        for section in body_text:
            hwp_section_stream = ole.openstream(section).read()
            hwp_section = zlib.decompress(hwp_section_stream, wbits=HWP_WBITS)

            utf8_str = hwp_section[1:-1].decode('utf-16-le', errors='replace')


import zlib

from olefile import OleFileIO

from spec.tag_id import HWPTAG_PARA_TEXT
from spec.record import DataRecord
from spec.info import MainText

HWP_WBITS = -15


def iter_text(stream):
    with OleFileIO(stream) as ole:
        body_text = ['/'.join(ls) for ls in ole.listdir() if 'BodyText' in ls]
        for section in body_text:
            hwp_section_stream = ole.openstream(section).read()
            hwp_section = zlib.decompress(hwp_section_stream, wbits=HWP_WBITS)
            record = DataRecord(hwp_section)
            for r in record:
                if r.tag_id == HWPTAG_PARA_TEXT:
                    yield from MainText(r.data)


def extract(hwp):
    with open(hwp, 'rb') as f:
        for o in iter_text(f):
            print(
                f"control={o.ctrl} "
                f"info={o.info} "
                f"text={o.data.decode('utf-16-le')}"
            )


if __name__ == '__main__':
    extract('example.hwp')

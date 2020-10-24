import zlib

from olefile import OleFileIO

from spec.tag_id import HWPTAG_PARA_TEXT
from spec.record import DataRecord

HWP_WBITS = -15


def iter_text(stream):
    with OleFileIO(stream) as ole:
        body_text = ['/'.join(ls) for ls in ole.listdir() if 'BodyText' in ls]
        for section in body_text:
            hwp_section_stream = ole.openstream(section).read()
            hwp_section = zlib.decompress(hwp_section_stream, wbits=HWP_WBITS)
            record = DataRecord(hwp_section)
            for r in record:
                print(HWPTAG_PARA_TEXT, r.tag_id, r)
                if r.tag_id == HWPTAG_PARA_TEXT:
                    yield r.data.decode('utf-16-le')


if __name__ == '__main__':
    with open('C:/Users/jongwony/Downloads/example.hwp', 'rb') as f:
        print(list(iter_text(f)))

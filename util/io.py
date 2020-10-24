import struct


def parse_header(b: bytes, condition: callable):
    header = struct.unpack('<I', b)[0]
    tag_id = header & 0x3ff
    header >>= 10
    level = header & 0x3ff
    header >>= 10
    size = header & 0xfff
    if condition(tag_id):
        return {
            'tag_id': tag_id,
            'level': level,
            'size': size,
        }

import argparse
from ctypes import *

# gzip has no padding format. but we can use File COMMENT entry to align deflate blocks
## see rfc1952


class Header(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('ID', c_char * 2),
        ('CM', c_uint8),
        ('FLG_FTEXT', c_uint8, 1),
        ('FLG_FHCRC', c_uint8, 1),
        ('FLG_FEXTRA', c_uint8, 1),
        ('FLG_FNAME', c_uint8, 1),
        ('FLG_FCOMMENT', c_uint8, 1),
        ('FLG_RESERVED', c_uint8, 3),
        ('MTIME', c_uint32),
        ('XFL', c_uint8),
        ('OS', c_uint8),
    ]


def read_null_terminated(src):
    buff = ''
    while True:
        x = src.read(1)
        if x == '\0':
            break
        buff += x
    return buff

def add_gzip(src, dst, size):
    h = Header()
    src.readinto(h)
    if h.ID != '\x1f\x8b':
        raise IOError('Not gzip')
    if h.FLG_FHCRC:
        print("WARN: Abandon header CRC.")
    if h.FLG_FEXTRA:
        xlen = c_uint16()
        src.readinto(xlen)
        ext = src.read(xlen)
    else:
        ext = None
    if h.FLG_FNAME:
        name = read_null_terminated(src)
        print("INFO: base file is '%s'" % name)
    else:
        name = None
    if h.FLG_FCOMMENT:
        comment = read_null_terminated(src)
        print("WARN: Orignal comment is deleted. '%s'" % name)
    h.FLG_FCOMMENT = 1
    dst.write(h)
    if ext:
        dst.write(xlen)
        dst.write(ext)
    if name:
        dst.write(name)
        dst.write('\0')
    dst.write('x' * size)
    dst.write('\0')
    dst.write(src.read())


parser = argparse.ArgumentParser(prog='gz_extend.py')
parser.add_argument('src', type=argparse.FileType('rb'))
parser.add_argument('dst', type=argparse.FileType('wb'))
parser.add_argument('size', type=int)


def main():
    args = parser.parse_args()
    add_gzip(args.src, args.dst, args.size)


if __name__ == '__main__':
    main()


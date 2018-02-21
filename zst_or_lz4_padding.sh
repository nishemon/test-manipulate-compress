#!/bin/sh

# LZ4 and Zstandard support the same Skippable Frames. Magic 0x184D2A5x
## https://github.com/lz4/lz4/wiki/lz4_Frame_format.md
## https://github.com/facebook/zstd/blob/dev/doc/zstd_compression_format.md


if [ $# -ne 3 ]; then
  echo "usage: $0 src dst size"
  echo "try > echo abc > abc"
  echo "try > zstd abc"
  echo "try > $0 abc.zst test.zst 100000"
  echo "try > zstd -cd test.zst"
  exit 1
fi

SRC=$1
DST=$2
SIZE=$3

cp $SRC $DST
python << EOS
import struct
# little endian magic(4bytes), size(4bytes)

with open('$DST', 'ab') as f:
     f.write(struct.pack('<LL', 0x184D2A50, $SIZE - 8))
EOS
dd if=/dev/zero bs=$[SIZE - 8] count=1 >> $DST
cat $SRC >> $DST


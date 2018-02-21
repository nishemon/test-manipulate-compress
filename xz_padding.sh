#!/bin/sh

# xz Stream Padding is simple all zero bytes.
## https://tukaani.org/xz/xz-file-format.txt

if [ $# -ne 3 ]; then
  echo "usage: $0 src dst size"
  echo "try > echo abc > abc"
  echo "try > xz abc"
  echo "try > $0 abc.xz test.xz 100000"
  echo "try > xzcat test.xz"
  exit 1
fi

SRC=$1
DST=$2
SIZE=$3

cp $SRC $DST
dd if=/dev/zero bs=$SIZE count=1 >> $DST
cat $SRC >> $DST


#!/usr/bin/env python3
"""news-23 b169 heroes-scene entry generator (stdlib only, no PIL).

Validates entry.png (PNG header via struct, chunk CRCs, size, sha256)
and writes it to $MAKEFUN_OUTPUT_DIR/entry.png only.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "4d4d099fe8ef99feae5a203b4b574c027280a03583d6810efcfb6b13e73383e2"
EXPECTED_SIZE = 138915

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
DST = os.path.join(DST_DIR, "entry.png")


def fail(msg):
    print("error:", msg, file=sys.stderr)
    sys.exit(1)


def validate(data):
    if len(data) < 10000:
        fail("too small: %d bytes" % len(data))
    if len(data) > 1024 * 1024:
        fail("too large: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    # first chunk must be IHDR, 13 bytes, 1024x1024, bit depth 8, color type 2/6
    off = 8
    length = struct.unpack(">I", data[off:off + 4])[0]
    ctype = data[off + 4:off + 8]
    if ctype != b"IHDR" or length != 13:
        fail("first chunk is not IHDR(13)")
    w, h, bd, ct, comp, filt, inter = struct.unpack(">IIBBBBB", data[off + 8:off + 21])
    if (w, h) != (1024, 1024):
        fail("bad dimensions: %dx%d" % (w, h))
    if bd != 8 or ct not in (2, 6):
        fail("bad bit depth / color type: %d / %d" % (bd, ct))
    if comp != 0 or filt != 0 or inter != 0:
        fail("bad compression/filter/interlace")
    if zlib.crc32(data[off + 4:off + 8 + 13]) & 0xFFFFFFFF != struct.unpack(
            ">I", data[off + 21:off + 25])[0]:
        fail("bad IHDR CRC")
    # walk chunks: CRC each, IDAT non-empty, IEND last with no trailing data
    off = 8
    idat_total = 0
    last = None
    while off < len(data):
        if off + 8 > len(data):
            fail("truncated chunk header")
        length = struct.unpack(">I", data[off:off + 4])[0]
        ctype = data[off + 4:off + 8]
        end = off + 8 + length + 4
        if end > len(data):
            fail("truncated chunk %r" % ctype)
        crc_stored = struct.unpack(">I", data[off + 8 + length:off + 12 + length])[0]
        crc_calc = zlib.crc32(data[off + 4:off + 8 + length]) & 0xFFFFFFFF
        if crc_stored != crc_calc:
            fail("bad CRC in chunk %r" % ctype)
        if ctype == b"IDAT":
            if length == 0:
                fail("empty IDAT chunk")
            idat_total += length
        last = ctype
        off = end
    if last != b"IEND":
        fail("last chunk is not IEND")
    if idat_total < 1000:
        fail("IDAT payload too small: %d" % idat_total)


def main():
    if not DST_DIR:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    if os.path.isfile(DST_DIR):
        fail("MAKEFUN_OUTPUT_DIR is a file")
    repo = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(DST_DIR) == repo or os.path.abspath(DST_DIR).startswith(repo + os.sep):
        fail("MAKEFUN_OUTPUT_DIR is inside the repo")
    if os.path.abspath(DST) == os.path.abspath(SRC):
        fail("output would overwrite source")
    try:
        with open(SRC, "rb") as f:
            data = f.read()
    except OSError as e:
        fail("cannot read source entry.png: %s" % e)
    validate(data)
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 != "PENDING" and sha != EXPECTED_SHA256:
        fail("sha256 mismatch: %s" % sha)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        fail("size mismatch: %d" % len(data))
    os.makedirs(DST_DIR, exist_ok=True)
    with open(DST, "wb") as f:
        f.write(data)
    with open(DST, "rb") as f:
        out = f.read()
    if out != data:
        fail("output is not byte-identical to source")
    print("wrote %s (%d bytes, sha256 %s)" % (DST, len(data), sha))


if __name__ == "__main__":
    main()

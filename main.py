#!/usr/bin/env python3
"""Sum Up 21 — make.fun news-image-20261121 entry runner.

Stdlib only. Copies the shipped entry.png (the rendered 21 November 2026
broadsheet front page) to the make.fun output directory byte-for-byte and
verifies the copy's SHA-256 against the shipped file.

Output directory: $MAKEFUN_OUTPUT_DIR, default /output.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_NAME = "entry.png"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, DST_NAME)
    if not os.path.isfile(SRC):
        print("missing shipped entry.png next to main.py", file=sys.stderr)
        return 1
    want = sha256_of(SRC)
    shutil.copyfile(SRC, dst)
    got = sha256_of(dst)
    if got != want:
        print("SHA-256 mismatch after copy: %s != %s" % (got, want),
              file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, os.path.getsize(dst), got))
    print("entry: Sum Up 21 — Saturday 21 November 2026, 38 stories, 13 drawn")
    return 0


if __name__ == "__main__":
    sys.exit(main())

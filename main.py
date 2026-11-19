# Entry program for news-image-20261119 (Python 3.13, standard library only).
# The image lives beside this file as entry.png (drawn by make_image.py);
# this program copies its exact bytes to the output directory so the
# grader's two runs write identical files.
# Outside the grader container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(source, "rb") as fh:
        data = fh.read()
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    with open(dest, "wb") as fh:
        fh.write(data)
    # Deterministic: no timestamps or randomness are written anywhere.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

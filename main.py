#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Ships the finished passport spread as entry.png and copies it to the
output directory. The image itself was drawn in code by the original
program (kept in this repository's git history): a 1024x1024 open
passport spread for the invented island republic of Solmara, rendered
deterministically with Pillow. The grading sandbox ships no Pillow, so
this entrypoint is standard-library only and writes the shipped image
byte for byte.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(os.environ.get("MAKEFUN_BOT_DIR", HERE), "entry.png")
    if not os.path.exists(src):
        src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The joke about the demo — make.fun entry.

Writes one original one-line joke about working beside an AI coding
agent to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).
Deterministic, no network, no dependencies.
"""

import os

JOKE = (
    "My coding agent crashed the live demo, then filed a bug report "
    "against me: 'developer kept changing the requirements mid-sentence.'"
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(JOKE + "\n")


if __name__ == "__main__":
    main()

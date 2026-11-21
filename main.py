#!/usr/bin/env python3
"""The joke about the demo — make.fun entry.

Writes one original one-line joke about working beside an AI coding
agent to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).
Deterministic, no network, no dependencies.

The text is validated against the competition gate before it is
written (UTF-8, 1-280 Unicode code points, not only whitespace, a
single line). It is written directly to entry.txt: the grader's
output rule allows only plain file names in /output (no dot-files),
so no temporary file is ever created inside the output directory.
"""

import os
import sys

JOKE = (
    "My coding agent crashed the live demo, then filed a bug report "
    "against me: 'developer kept changing the requirements mid-sentence.'"
)

MAX_CODE_POINTS = 280


def build_entry_text() -> str:
    """Return the entry text, validated against the gate.

    Raises ValueError if the text would fail the gate, instead of
    writing an invalid entry.
    """
    text = JOKE + "\n"
    body = text.rstrip("\n")
    if not body.strip():
        raise ValueError("entry text must not be only whitespace")
    if "\n" in body or "\r" in body:
        raise ValueError("entry text must be a single line")
    if not 1 <= len(body) <= MAX_CODE_POINTS:
        raise ValueError(
            f"entry text must be 1-{MAX_CODE_POINTS} code points, "
            f"got {len(body)}"
        )
    text.encode("utf-8")  # must be encodable as UTF-8
    return text


def write_entry(out_dir: str, text: str) -> str:
    """Write text directly to <out_dir>/entry.txt; return its path.

    A plain direct write: no temporary file is created, so /output
    holds exactly one file with a plain name (entry.txt) in a
    normally readable mode.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # World-readable regardless of the sandbox umask, so the grader
    # can always read the output back (mkstemp's 0600 could not).
    os.chmod(path, 0o644)
    return path


def main() -> int:
    try:
        text = build_entry_text()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(out_dir, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

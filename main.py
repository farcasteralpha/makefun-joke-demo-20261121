#!/usr/bin/env python3
"""The joke about the demo — make.fun entry.

Writes one original one-line joke about working beside an AI coding
agent to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).
Deterministic, no network, no dependencies.

The text is validated against the competition gate before it is
written (UTF-8, 1-280 Unicode code points, not only whitespace, a
single line), and it is written atomically so a reader never sees a
half-written file.
"""

import os
import sys
import tempfile

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
    """Write text atomically to <out_dir>/entry.txt; return its path."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(
        dir=out_dir, prefix=".entry.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
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

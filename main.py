#!/usr/bin/env python3
"""Famous Last Words at 1 Percent - writes one funny last-words line.

The line is what a phone would say as its battery hits 1 percent: a
single line of at most 199 characters. Deterministic: no network,
no randomness, no clock.
"""

import os

LINE = (
    "I survived drops, water, and your 47 open tabs \u2014 but 1% is where "
    "my story ends. Tell Siri I said nothing. She never listens anyway."
)

MAX_CHARS = 199


def validate(line: str) -> bytes:
    """Check the line against the brief and return its exact UTF-8 bytes."""
    if not line:
        raise SystemExit("Invalid line: entry must be non-empty.")
    if line != line.strip():
        raise SystemExit(
            "Invalid line: entry must not have leading or trailing whitespace."
        )
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"Invalid line: {len(line)} characters, over the {MAX_CHARS} limit."
        )
    if "\n" in line or "\r" in line:
        raise SystemExit(
            "Invalid line: entry must be a single line with no newline characters."
        )
    bad = [c for c in line if ord(c) < 0x20 or ord(c) == 0x7F]
    if bad:
        raise SystemExit(
            f"Invalid line: contains control character(s): {[hex(ord(c)) for c in bad]}."
        )
    return line.encode("utf-8")


def main() -> None:
    expected = validate(LINE)
    output_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(expected)
    with open(output_path, "rb") as f:
        written = f.read()
    if written != expected:
        raise SystemExit(
            "Write verification failed: entry file bytes do not match the line."
        )
    if written.decode("utf-8") != LINE:
        raise SystemExit(
            "Write verification failed: entry file text does not match the line."
        )


if __name__ == "__main__":
    main()

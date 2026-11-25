#!/usr/bin/env python3
"""
fix_bidi.py - Bidirectional (BiDi) Persian/English Markdown Formatter for Antigravity.

Fixes common word-order scrambling issues in mixed Persian (RTL) and English (LTR)
Markdown texts by:
1. Detecting paragraphs containing Persian characters.
2. Inserting Right-to-Left Marks (RLM, U+200F) after inline LTR tokens or backtick spans
   when followed by neutral punctuation or another LTR span in an RTL line.
3. Prefixing RTL lines that begin with an English term/backtick with RLM so the
   paragraph base direction remains RTL.
"""

import argparse
import re
import sys
from pathlib import Path

RLM = "\u200f"  # Right-to-Left Mark
PERSIAN_RE = re.compile(r"[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]")
LATIN_SPAN_RE = re.compile(r"(`[^`]+`|\b[A-Za-z][A-Za-z0-9_./:@+-]*\b)")


def has_persian(text: str) -> bool:
    return bool(PERSIAN_RE.search(text))


def starts_with_ltr(line: str) -> bool:
    stripped = re.sub(r"^(\s*(?:[-*+]|\d+\.)\s+|\s*#+\s+|\s*>\s+)", "", line)
    if not stripped:
        return False
    first_char = stripped[0]
    return ("A" <= first_char <= "Z") or ("a" <= first_char <= "z") or first_char == "`"


def fix_rtl_line(line: str) -> str:
    if not has_persian(line):
        return line

    # If an RTL line starts with an LTR token or backtick (after list/heading markers),
    # insert an RLM right after the list/heading marker so renderers keep the line RTL.
    marker_match = re.match(r"^(\s*(?:[-*+]|\d+\.)\s+|\s*#+\s+|\s*>\s+)?(.*)$", line)
    prefix = marker_match.group(1) or ""
    body = marker_match.group(2)

    if body and not body.startswith(RLM) and starts_with_ltr(body):
        body = RLM + body

    # Add RLM after inline code spans or Latin words when followed by neutral punctuation
    # and another Latin word or end-of-clause in a Persian line.
    def add_rlm_after_latin(match: re.Match) -> str:
        token = match.group(0)
        return token + RLM

    body = LATIN_SPAN_RE.sub(add_rlm_after_latin, body)
    # Deduplicate consecutive RLMs
    body = re.sub(f"{RLM}+", RLM, body)
    return prefix + body


def process_markdown(content: str) -> str:
    lines = content.splitlines(keepends=True)
    out = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            out.append(line)
            continue

        if in_code_block or stripped.startswith("<"):
            out.append(line)
            continue

        out.append(fix_rtl_line(line))

    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix bidirectional (BiDi) word-order scrambling in mixed Persian/English Markdown."
    )
    parser.add_argument("file", help="Path to Markdown file (or '-' for stdin)")
    parser.add_argument(
        "--in-place", "-i", action="store_true", help="Modify the file in-place"
    )
    args = parser.parse_args()

    if args.file == "-":
        sys.stdout.write(process_markdown(sys.stdin.read()))
        return 0

    path = Path(args.file)
    content = path.read_text(encoding="utf-8")
    fixed = process_markdown(content)

    if args.in_place:
        path.write_text(fixed, encoding="utf-8")
    else:
        sys.stdout.write(fixed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

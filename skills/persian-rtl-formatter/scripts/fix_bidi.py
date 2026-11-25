#!/usr/bin/env python3
"""
fix_bidi.py - Bidirectional (BiDi) Persian/English Markdown Formatter for Antigravity.

Fixes left-alignment and word-order scrambling in mixed Persian (RTL) and English (LTR)
Markdown texts rendered under `dir="auto"` / `unicode-bidi: plaintext` by:
1. Detecting lines/paragraphs containing Persian characters.
2. Detecting when the first strong directional character of an RTL line is Latin
   (including inside **bold**, *italic*, `code`, [links](url), or bare URLs) and
   inserting a raw Unicode Right-to-Left Mark (RLM, U+200F) right after any Markdown
   list/heading/blockquote prefix so `dir="auto"` keeps the entire line RTL.
3. Isolating inline Latin/code runs inside Persian lines with Unicode Left-to-Right
   Isolate (LRI, U+2066) ... Pop Directional Isolate (PDI, U+2069) so neutral
   punctuation and adjacent English spans never scramble surrounding Persian words.
"""

import argparse
import re
import sys
from pathlib import Path

RLM = "\u200f"  # Right-to-Left Mark (BiDi class R - Strong RTL)
LRI = "\u2066"  # Left-to-Right Isolate
PDI = "\u2069"  # Pop Directional Isolate

PERSIAN_RE = re.compile(r"[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]")
STRONG_CHAR_RE = re.compile(r"([A-Za-z]|[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF\u200F])")
# Matches inline code spans, markdown links, or Latin word/identifier runs
INLINE_LTR_RE = re.compile(
    r"(`[^`]+`|\[[^\]]+\]\([^)]+\)|https?://\S+|\b[A-Za-z][A-Za-z0-9_./:@+-]*\b)"
)
PREFIX_RE = re.compile(r"^(\s*(?:[-*+]|\d+\.|[۰-۹]+\.)\s+|\s*#+\s+|\s*>\s+)?(.*)$")


def has_persian(text: str) -> bool:
    return bool(PERSIAN_RE.search(text))


def first_strong_is_ltr(text: str) -> bool:
    # Strip markdown emphasis/brackets/backticks to find the first rendered strong char
    cleaned = re.sub(r"(\*\*|__|\*|_|`|\[|\]\(.*?\))", "", text)
    match = STRONG_CHAR_RE.search(cleaned)
    if not match:
        return False
    ch = match.group(1)
    return ("A" <= ch <= "Z") or ("a" <= ch <= "z")


def isolate_inline_ltr(text: str) -> str:
    def _wrap(match: re.Match) -> str:
        token = match.group(0)
        # Skip markdown links whose visible label is already Persian
        if token.startswith("[") and "](" in token:
            label = token[1 : token.index("](")]
            if has_persian(label) and not first_strong_is_ltr(label):
                return token
        return f"{LRI}{token}{PDI}"

    # Avoid double-wrapping already isolated spans
    if LRI in text and PDI in text:
        return text
    return INLINE_LTR_RE.sub(_wrap, text)


def fix_rtl_line(line: str) -> str:
    ending = ""
    if line.endswith("\r\n"):
        ending = "\r\n"
        core = line[:-2]
    elif line.endswith("\n"):
        ending = "\n"
        core = line[:-1]
    else:
        core = line

    if not has_persian(core):
        return line

    match = PREFIX_RE.match(core)
    prefix = match.group(1) or ""
    body = match.group(2)

    if not body:
        return line

    needs_leading_rlm = not body.startswith(RLM) and first_strong_is_ltr(body)
    body = isolate_inline_ltr(body)

    if needs_leading_rlm:
        body = RLM + body

    return prefix + body + ending


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
        description="Fix bidirectional (BiDi) left-alignment and word-order scrambling in mixed Persian/English Markdown."
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

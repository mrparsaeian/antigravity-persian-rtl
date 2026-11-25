---
name: persian-rtl-formatter
description: Comprehensive guide and utility scripts for formatting mixed Persian (Farsi) and English bidirectional (BiDi) text, fixing left-aligned/scrambled sentences in Antigravity chat and Markdown documents.
---

# Persian RTL & BiDi Formatter Skill

Use this skill when the user asks to format, debug, or fix mixed Persian/English documents, Markdown files, chat outputs, or HTML/Generative UI widgets so that Right-to-Left (RTL) text and Left-to-Right (LTR) technical terms render in the exact intended reading order without flipping left-aligned or scrambling.

## Why Mixed Persian/English Lines Flip Left-Aligned in Chat UIs
1. **Sanitized Markdown strips raw HTML**: Most chat Markdown renderers (including Antigravity's chat canvas) strip or ignore raw HTML tags like `<div dir="rtl">` and `<bdi dir="ltr">`, and instead rely on HTML `dir="auto"` / CSS `unicode-bidi: plaintext` per block (`<p>`, `<li>`, `<h1>-<h6>`).
2. **First-Strong-Character Heuristic (Unicode UAX #9 P2/P3)**: Under `dir="auto"`, the browser inspects each paragraph or list item for its *first strong directional character*:
   - Persian/Arabic letter (`R`/`AL`) → Paragraph becomes **RTL (right-aligned)**.
   - Latin letter (`L`), even inside `**bold**`, `` `code` ``, or `[links](...)` → Paragraph becomes **LTR (left-aligned)** and scrambles the word order!
3. **Neutral characters between English spans**: Spaces, hyphens (`-`), slashes (`/`), colons (`:`), and parentheses `()` are directionally neutral. Two English words separated only by neutral characters merge into a single LTR run and flip relative positions in an RTL sentence.

## How to Guarantee Clean RTL Output

### 1. In Chat & Markdown (Pure Unicode + Persian-First)
- **Always start every Persian paragraph, heading, list item, and table cell with a Persian word.**
- **When a line must start with an English word, code span, or URL**, prepend the actual raw Unicode Right-to-Left Mark (`\u200F` / `‏`), NOT the HTML entity `&rlm;`. Because `U+200F` has Unicode BiDi class `R` (Strong RTL), `dir="auto"` treats the entire paragraph as RTL!
- **For inline English multi-word phrases**, isolate them with Unicode Left-to-Right Isolate (`\u2066`) ... Pop Directional Isolate (`\u2069`) or backticks + Persian connectors, and never place two unisolated English tokens back-to-back with only neutral punctuation.

### 2. In HTML / Generative UI Widgets
When generating actual HTML (not sanitized chat Markdown):
- Set `dir="rtl"` and `style="direction: rtl; text-align: right;"` on Persian containers.
- Set `dir="ltr" style="unicode-bidi: isolate;"` on code and English spans.

### 3. Fixing Existing Markdown Files Automatically
Run the bundled script `scripts/fix_bidi.py` to automatically repair mixed Persian/English Markdown files (prepends raw `U+200F` on any Persian line that starts with English/bold/code/link and isolates inline LTR spans with `U+2066`...`U+2069` + `U+200F`):

```bash
python3 ~/.gemini/config/plugins/persian-rtl/skills/persian-rtl-formatter/scripts/fix_bidi.py <input_file.md> --in-place
```

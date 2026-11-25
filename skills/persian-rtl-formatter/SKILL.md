---
name: persian-rtl-formatter
description: Comprehensive guide and utility scripts for formatting mixed Persian (Farsi) and English bidirectional (BiDi) text, fixing scrambled word order in Markdown/HTML outputs, and converting existing documents to clean RTL.
---

# Persian RTL & BiDi Formatter Skill

Use this skill when the user asks to format, fix, or convert mixed Persian/English documents, Markdown files, artifacts, or UI components so that Right-to-Left (RTL) text and Left-to-Right (LTR) technical terms render in the exact intended reading order without scrambling.

## Why Mixed Persian/English Text Scrambles
Under the Unicode Bidirectional Algorithm (UBA):
1. **Paragraph base direction**: Many Markdown renderers determine paragraph direction from the first strong character, or default to `dir="ltr"`. When a Persian paragraph is rendered in an LTR container, punctuation at the end of the sentence jumps to the right, and starting a line with an English word flips the entire line to LTR.
2. **Neutral characters between LTR tokens**: Characters like spaces, colons (`:`), hyphens (`-`), slashes (`/`), and parentheses `()` are directionally neutral. When two English terms sit near each other with only neutral characters or short punctuation between them, the renderer merges them into a single LTR run and reverses their relative order in a Persian sentence.

## Best Practices for Clean BiDi Output

### 1. Block-Level RTL Containers
Wrap Persian sections in `<div dir="rtl" align="right">`:
```markdown
<div dir="rtl" align="right">

در این بخش تنظیمات مربوط به فایل `platformio.ini` و نحوه کامپایل پروژه روی برد `ESP32-S3` را بررسی می‌کنیم.

</div>
```
Always close `<div dir="rtl">` before opening a fenced code block (` ``` `) and reopen it afterward so code blocks stay strictly LTR.

### 2. Inline Technical Spans
- Wrap single technical tokens, filenames, commands, and versions in backticks: `` `agy --version` ``, `` `v2.35.1` ``.
- Wrap multi-word non-code English phrases in `<bdi dir="ltr">...</bdi>` so their internal LTR order is preserved while their position inside the Persian sentence follows RTL flow.

### 3. Fixing Existing Markdown Files Automatically
You can run the bundled Python formatter script `scripts/fix_bidi.py` to automatically fix mixed Persian/English Markdown files (adds RTL markers around unisolated LTR runs and optionally wraps Persian blocks in `<div dir="rtl">`):

```bash
python3 ~/.gemini/config/plugins/persian-rtl/skills/persian-rtl-formatter/scripts/fix_bidi.py <input_file.md> --in-place
```

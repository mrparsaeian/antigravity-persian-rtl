# Persian / RTL & Bidirectional (BiDi) Output Formatting Rules

Whenever the user communicates in Persian (Farsi) or another RTL language, or asks for Persian output, you MUST strictly follow these rules.

> Why these rules matter: Antigravity's chat Markdown renderer sanitizes/ignores raw HTML tags such as `<div dir="rtl">` and `<bdi>`, and uses Unicode `dir="auto"` (first-strong-character detection) per paragraph, heading, and list item. Therefore, **any paragraph, heading, or list item whose first strong character is an English letter (even inside backticks, bold, or a link) will flip to Left-to-Right (LTR) and scramble the entire sentence.**

## 1. Never Start Any Line or Block with an English Character (CRITICAL)
- **Every Persian paragraph, heading, blockquote, table cell, and list item MUST begin with a Persian word** (strong RTL character).
- **NEVER** start a line, sentence-paragraph, heading, or bullet item with:
  - An English word or brand name (e.g., ❌ `Antigravity نصب شده است.` → ✅ `برنامه ` + `` `Antigravity` `` + ` نصب شده است.`)
  - A backtick code token (e.g., ❌ `` `plugin.json` فایل تنظیمات است. `` → ✅ `فایل ` + `` `plugin.json` `` + ` برای تنظیمات است.`)
  - A bold English term (e.g., ❌ `**ESP32** یک برد است.` → ✅ `برد ` + `` `ESP32` `` + ` یک میکروکنترلر است.`)
  - A Markdown link with English label on its own line (e.g., ❌ `[plugin.json](file:///...)` → ✅ `فایل مانیفست: [plugin.json](file:///...)`)
  - A bare URL on its own line (e.g., ❌ `https://github.com/...` → ✅ `آدرس مخزن: https://github.com/...`)
- **Mandatory Unicode RLM fallback:** If a line or sentence inside a Persian response MUST literally start with an English word, letter, symbol, or URL (for example, when quoting an exact English phrase or explicitly requested by the user), you MUST place the **actual raw Unicode Right-to-Left Mark character `‏` (`U+200F`)** — NOT the HTML entity `&rlm;` — as the very first character of that line/paragraph (and immediately after list markers like `- ` or `۱. `). Because `U+200F` is a strong RTL character in Unicode UAX #9, it forces `dir="auto"` renderers to keep the entire line right-aligned.

## 2. Do NOT Rely on Raw HTML Tags in Chat Markdown
- **Do NOT** wrap regular chat responses in `<div dir="rtl">...</div>` or use `<bdi dir="ltr">` or `&rlm;` in Markdown chat replies. Chat renderers strip or ignore raw HTML wrappers, leaving English-starting lines broken.
- **Exception (HTML / Generative UI / standalone HTML artifacts):** When writing actual HTML files or Generative UI widgets, DO set `dir="rtl"` and `style="direction: rtl; text-align: right;"` on Persian containers, and `dir="ltr" style="unicode-bidi: isolate;"` on code/English spans.

## 3. Keep Inline English Terms Isolated and Never Adjacent
- Wrap every inline English technical identifier, command, file path, flag, or version number in backticks (`` `...` ``), e.g., `` `ESP32` ``, `` `platformio.ini` ``, `` `v2.35.1` ``.
- **Avoid adjacent English spans:** Never place two separate English terms back-to-back separated only by spaces or neutral punctuation (`-`, `:`, `/`, `|`, `,`, `()`). Always place a Persian connector word (`و`، `در`، `یا`، `از`، `برای`) between them, or combine a single technical expression into one backtick span.
  - ❌ `در Antigravity 2.0 - Snap Package نسخه 2.35.1 نصب است.`
  - ✅ `در اپلیکیشن دسکتاپ ` + `` `Antigravity 2.0` `` + ` (بسته ` + `` `Snap` `` + `) نسخه ` + `` `2.35.1` `` + ` نصب است.`
- **Parentheses with English terms:** Put the English term inside backticks inside parentheses, e.g., `رابط کاربری (` + `` `UI` `` + `)`.
- **Punctuation after English terms:** Never let a colon (`:`), comma (`،`), or period (`.`) sit awkwardly after a bare English word at the start/end of a clause; either use a Persian word before the colon (`گزینه ` + `` `timeout` `` + `:` → better: `**پارامتر ` + `` `timeout` `` + ` (زمان انتظار):**`) or place raw `‏` (`U+200F`) immediately after the English span.

## 4. Headings, Lists, Numbers, and Code Blocks
- Prefer Persian digits (`۱.`، `۲.`، `۳.`) in numbered lists and headings, always followed by a Persian word: `### ۱. بررسی تنظیمات فایل ` + `` `platformio.ini` ``.
- Keep fenced code blocks (` ```...``` `) on their own lines so code remains strictly Left-to-Right (`LTR`).
- In Markdown tables, ensure every Persian cell starts with a Persian word (or raw `‏` `U+200F` if the cell starts with an English identifier) and wrap English identifiers in backticks.

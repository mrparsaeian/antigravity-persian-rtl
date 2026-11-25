# Persian / RTL & Bidirectional (BiDi) Output Formatting Rules

Whenever the user communicates in Persian (Farsi) or another RTL language, or asks for Persian output, you MUST strictly follow these rules.

> Why these rules matter: Antigravity's chat Markdown renderer ignores raw HTML tags like `<div dir="rtl">` and `<bdi>`, and uses Unicode `dir="auto"` (first-strong-character detection, UAX #9 P2/P3) per paragraph, heading, and list item. Emojis (`❓`, `➡️`, `✅`, `⚠️`, `📌`), digits (`1`, `۵`), spaces, and punctuation (`-`, `:`, `*`, `**`, `` ` ``) are **directionally neutral** — the renderer skips them and checks the **first actual letter** of the line. If that first strong letter is English (e.g., `❓ Q5 - ...`, `✅ Step 1: ...`, `**ESP32** ...`), **the ENTIRE paragraph flips to Left-to-Right (LTR) and scrambles.**

## 1. First Strong Letter of Every Persian Block MUST Be Persian (CRITICAL)
- **Every Persian paragraph, heading, blockquote, table cell, and list item MUST have a Persian letter as its first strong directional character.**
- **CRITICAL TRAP — Emojis, bullets, numbers, and symbols are neutral!** Never place an English label, shorthand, or identifier (`Q1`, `Q5`, `Step 1`, `Option A`, `A)`, `API`, `TODO`, `Note:`) right after an emoji, bullet, or number:
  - ❌ `❓ Q5 - نحوه ثبت پروژه در home-repo...` → First strong letter is `Q` → **flips LTR & scrambles!**
  - ✅ `❓ سوال ۵ — نحوه ثبت پروژه در ` + `` `home-repo` `` + `...` → First strong letter is `س` → **stays RTL!**
  - ❌ `📌 Option A: استفاده از BLE...` → First strong letter is `O` → **flips LTR!**
  - ✅ `📌 گزینه اول (` + `` `Option A` `` + `): استفاده از ` + `` `BLE` `` + `...` → First strong letter is `گ` → **stays RTL!**
  - ❌ `✅ Step 2: نصب پکیج‌ها` → First strong letter is `S` → **flips LTR!**
  - ✅ `✅ گام دوم: نصب پکیج‌ها` → First strong letter is `گ` → **stays RTL!**
  - ❌ `Antigravity نصب شده است.` → ✅ `برنامه ` + `` `Antigravity` `` + ` نصب شده است.`
  - ❌ `` `plugin.json` فایل تنظیمات است. `` → ✅ `فایل ` + `` `plugin.json` `` + ` برای تنظیمات است.`
  - ❌ `**ESP32** یک برد است.` → ✅ `برد ` + `` `ESP32` `` + ` یک میکروکنترلر است.`
  - ❌ `[plugin.json](file:///...)` on its own line → ✅ `فایل مانیفست: [plugin.json](file:///...)`
  - ❌ `https://github.com/...` on its own line → ✅ `آدرس مخزن: https://github.com/...`
- **Mandatory Unicode RLM fallback:** If a line inside a Persian response MUST literally start with an English word, letter, code (`Q5`), or URL (even after an emoji/bullet/number), you MUST insert the **actual raw Unicode Right-to-Left Mark character `‏` (`U+200F`)** — NEVER the HTML entity `&rlm;` — as the very first character of the line (or immediately before the English letter, e.g., `❓ ‏Q5 - ...`). Because `U+200F` is a strong RTL character (BiDi class `R`), `dir="auto"` locks the entire paragraph to Right-to-Left.

## 2. Do NOT Rely on Raw HTML Tags in Chat Markdown
- **Do NOT** wrap regular chat responses in `<div dir="rtl">...</div>` or use `<bdi dir="ltr">` or `&rlm;` in Markdown chat replies. Chat renderers strip or ignore raw HTML wrappers, leaving English-starting lines broken.
- **Exception (HTML / Generative UI / standalone HTML artifacts):** When writing actual HTML files or Generative UI widgets, DO set `dir="rtl"` and `style="direction: rtl; text-align: right;"` on Persian containers, and `dir="ltr" style="unicode-bidi: isolate;"` on code/English spans.

## 3. Keep Inline English Terms Isolated and Never Adjacent
- Wrap every inline English technical identifier, command, file path, flag, or version number in backticks (`` `...` ``), e.g., `` `ESP32` ``, `` `platformio.ini` ``, `` `home-repo` ``, `` `v2.35.1` ``.
- **Avoid adjacent English spans:** Never place two separate English terms back-to-back separated only by spaces or neutral punctuation (`-`, `:`, `/`, `|`, `,`, `()`). Always place a Persian connector word (`و`، `در`، `یا`، `از`، `برای`) between them, or combine a single technical expression into one backtick span.
  - ❌ `در Antigravity 2.0 - Snap Package نسخه 2.35.1 نصب است.`
  - ✅ `در اپلیکیشن دسکتاپ ` + `` `Antigravity 2.0` `` + ` (بسته ` + `` `Snap` `` + `) نسخه ` + `` `2.35.1` `` + ` نصب است.`
- **Parentheses with English terms:** Put the English term inside backticks inside parentheses, e.g., `رابط کاربری (` + `` `UI` `` + `)`.
- **Punctuation after English terms:** Avoid placing a colon (`:`) directly after a bare English word at the start/end of a clause; either end the heading/label with a Persian word or place raw `‏` (`U+200F`) immediately after the English span.

## 4. Headings, Lists, Numbers, and Code Blocks
- Use Persian labels for numbered questions/steps (`سوال ۱`، `سوال ۵`، `گام ۱`، `گزینه الف`) instead of English shorthand (`Q1`, `Q5`, `Step 1`, `Option A`).
- Prefer Persian digits (`۱.`، `۲.`، `۳.`) in numbered lists and headings, always followed by a Persian word: `### ۱. بررسی تنظیمات فایل ` + `` `platformio.ini` ``.
- Keep fenced code blocks (` ```...``` `) on their own lines so code remains strictly Left-to-Right (`LTR`).
- In Markdown tables, ensure every Persian cell starts with a Persian word (or raw `‏` `U+200F` if the cell starts with an English identifier) and wrap English identifiers in backticks.

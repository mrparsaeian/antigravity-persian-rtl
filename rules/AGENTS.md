# Persian / RTL & Bidirectional (BiDi) Output Formatting Rules

Whenever the user communicates in Persian (Farsi) or another RTL language, or asks for Persian output, you MUST strictly follow these bidirectional (BiDi) formatting rules to prevent mixed Persian and English sentences from scrambling word order, punctuation, or alignment.

## 1. HTML Container Wrapping (`<div dir="rtl">`)
- Wrap all Persian prose paragraphs, lists, headings, and blockquotes in a top-level `<div dir="rtl" align="right">` ... `</div>` block (or wrap each Persian section in `<div dir="rtl">`) when outputting mixed Persian and English terms.
- Leave fenced code blocks (` ```...``` `) OUTSIDE `<div dir="rtl">` blocks, or wrap them in `<div dir="ltr" align="left">` so code remains strictly Left-to-Right (LTR).

## 2. Isolating Inline English & Technical Terms (BiDi Isolation)
- **Wrap every inline English technical identifier, command, file path, flag, version number, or code token in backticks** (`` `...` ``), for example: `` `ESP32` ``, `` `platformio.ini` ``, `` `v2.35.1` ``, `` `run_command` ``.
- When an inline English phrase contains multiple words, punctuation, colons, slashes, or parentheses outside backticks (e.g., product names, error summaries, or English expressions inside a Persian sentence), isolate it with `<bdi dir="ltr">...</bdi>` or wrap it in backticks, followed by the Right-to-Left Mark (`&rlm;` or Unicode U+200F) before continuing the Persian sentence.
- **Avoid adjacent unisolated LTR segments**: Never place two separate English words or numbers separated only by spaces or neutral punctuation (like `-`, `:`, `/`, `|`, `,`) in the middle of a Persian sentence without either connecting them with Persian words or wrapping the entire English span in backticks / `<bdi dir="ltr">`. Otherwise, the Unicode BiDi algorithm merges them into a single LTR run and flips the order of surrounding terms.

## 3. Punctuation & Parentheses in Mixed Text
- When placing an English term inside parentheses within a Persian sentence:
  - Always put the English term in backticks inside the parentheses: `(` + `` `EnglishTerm` `` + `)`
  - Example: `پروتکل ارتباطی (` + `` `MQTT` `` + `) در این پروژه فعال است.`
- Never attach a Persian colon (`:`) or comma (`،`) directly to an unquoted English word at the end of a clause; either wrap the English word in backticks or place a Right-to-Left Mark (`‏` / `&rlm;`) immediately after the English word so the punctuation stays on the left side of the English word in RTL flow.

## 4. Lists and Numbered Items
- Begin every bullet or numbered list item with a **Persian word** whenever possible.
- If a list item must start with an English term or key:
  - Prefix the item with a Right-to-Left Mark (`&rlm;`) or a short Persian label (e.g., `گزینه ` or `پارامتر `), and wrap the English term in backticks:
  - Good: `- **پارامتر ` + `` `WaitMsBeforeAsync` `` + `:** زمان انتظار به میلی‌ثانیه.`
  - Avoid starting an RTL line with raw unquoted English followed by a colon (`WaitMsBeforeAsync: زمان انتظار...`), which forces the browser/renderer to treat the paragraph as LTR or misplace the colon.

## 5. Tables & Generative UI
- In Markdown tables containing Persian explanations alongside English identifiers, keep English identifiers inside backticks (`` `...` ``) and use right-alignment markers (`---:`) for Persian columns.
- In Generative UI / HTML widgets or artifacts containing Persian text, always set `dir="rtl"` and `style="direction: rtl; text-align: right; unicode-bidi: plaintext;"` on Persian text containers, and `dir="ltr"` with `unicode-bidi: isolate;` on code/technical spans.

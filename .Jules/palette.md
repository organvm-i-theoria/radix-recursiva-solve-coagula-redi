## 2025-12-14 - [Visual Hierarchy in CLI Tools]
**Learning:** CLI tools often dump raw JSON or mixed log output, making it hard for users to parse critical information. By adding semantic coloring (Green=Success, Red=Failure, Cyan=Keys) and structured indentation, we can significantly reduce cognitive load without changing functionality.
**Action:** When working on CLIs, always create a simple `Colors` helper and format complex objects (like status reports) into human-readable key-value pairs instead of raw JSON dumps. Also, ensure internal logging is suppressed or redirected so it doesn't pollute the user's primary interface.

## 2026-01-18 - [ANSI Codes and Text Wrapping]
**Learning:** Python's `textwrap` module counts invisible ANSI escape codes as visible characters, leading to incorrect line wrapping and short lines. Additionally, putting ANSI codes in `subsequent_indent` causes them to be counted repeatedly, confusing the wrapper.
**Action:** When implementing colored borders or indentation in wrapped text, apply the wrapping logic to the *plain* text first, then manually prepend the colored border/indentation to each resulting line during the print loop. Do not pass colored strings to `textwrap` parameters.

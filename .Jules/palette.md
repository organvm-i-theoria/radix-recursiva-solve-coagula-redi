## 2026-01-17 - Unifying CLI Styling
**Learning:** Inconsistent UI patterns (emojis vs cards, hardcoded vs shared colors) create a disjointed user experience even in CLI tools. Centralizing styling logic (`habitat_ux`) early prevents drift.
**Action:** When auditing CLI tools, look for "rogue" print statements that bypass the established UX module and refactor them to use shared components (`print_card`, `Colors`).

## 2026-01-17 - The Cost of Hardcoded Strings
**Learning:** Hardcoded "intro" strings in Python's `cmd` module limit dynamic styling opportunities (like ANSI colors).
**Action:** Use the `preloop` hook to render dynamic, styled headers instead of relying on the static `intro` attribute.

## 2026-01-20 - Feedback in Ephemeral CLI Tools
**Learning:** Even in stateless or ephemeral CLI tools, users expect immediate visual feedback for blocking operations. A simple spinner reduces uncertainty about whether the tool has hung.
**Action:** Implement threading-based spinners for any CLI operation expected to take more than 500ms, ensuring they clean up their own ANSI artifacts.

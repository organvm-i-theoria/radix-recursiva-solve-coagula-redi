# Palette's Journal - UX & Accessibility Learnings

## 2025-12-16 - CLI Output Formatting
**Learning:** Raw JSON dumps in CLI tools are functionally complete but cognitively overloading for users. Simple tabular alignment and columnar layouts significantly improve scannability without sacrificing data density.
**Action:** When building CLIs, always wrap JSON/dict outputs with a structured formatter (like `_print_kv` or table view) for the default human-readable mode, while keeping the return value programmatic.
## 2025-12-15 - [Safety Confirmation]
**Learning:** Destructive CLI actions like `cleanup` should always require explicit confirmation to prevent accidental data loss.
**Action:** Implement `input()` check before proceeding with `cleanup_all`, and add a `--force` flag for scripts.

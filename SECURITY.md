# Security Policy

## Supported Versions

This project is currently under active development. Security updates are applied to the main branch.

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Recent Security Fixes

### Path Traversal Vulnerability (Fixed: Dec 2025)
- **Component**: `experimental_habitat_implementation.py`
- **Severity**: HIGH
- **Issue**: Unsanitized experiment names could escape containment directories
- **Fix**: Strict input validation with alphanumeric whitelist
- **Details**: See [SECURITY_FIX_DOCUMENTATION.md](./SECURITY_FIX_DOCUMENTATION.md)

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it by:

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Email the maintainers directly or use GitHub's private vulnerability reporting
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline
- **Initial Response**: Within 48 hours
- **Status Update**: Weekly until resolved
- **Fix Timeline**: Critical issues within 7 days, others within 30 days

### What to Expect
- **Accepted**: We'll work with you on a fix and coordinate disclosure
- **Declined**: We'll explain why we don't consider it a vulnerability
- **Credit**: Security researchers will be credited (unless they prefer anonymity)

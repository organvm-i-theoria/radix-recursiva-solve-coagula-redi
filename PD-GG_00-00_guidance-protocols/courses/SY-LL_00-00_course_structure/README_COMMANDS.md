# Course Utility Script Index

These tools support the automation and modular expansion of your ENG101 course system.

## 1. `uid_check.py`
**Function:**
Scans all `.md` files in a directory for UID strings using the `AB-CD_12-34` pattern. Reports duplicates or malformed entries.

**Usage:**
```bash
python uid_check.py
```
Run from the base folder where your `.md` files live.

---

## 2. `zip_unit.py`
**Function:**
Zips a single unit folder (e.g. `NRTV0100_narrative_essay`) for export or LMS upload.

**Usage:**
```bash
python zip_unit.py NRTV0100_narrative_essay
```
Creates `NRTV0100_narrative_essay_FULL.zip` in the current directory.

---

## 3. `course_clone.py`
**Function:**
Duplicates an entire course folder (e.g. `ENG101_AMP_24FA`) and prepares it for a new semester or iteration.

**Usage:**
```bash
python course_clone.py ENG101_AMP_24FA ENG101_AMP_25SP
```
Copies the full structure and files from the original folder into a new one.

---

## Notes
- These are base-level prototypes. Additional features (UID bumping, internal refactoring, symbolic re-indexing) can be added.
- Scripts can be expanded into GUI-based or shell-integrated workflows.

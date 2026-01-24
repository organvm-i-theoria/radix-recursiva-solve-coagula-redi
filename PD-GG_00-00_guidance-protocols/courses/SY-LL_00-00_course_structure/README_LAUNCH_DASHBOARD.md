# ENG101 Launch Dashboard

This is your master deployment guide for the fully UID-structured, modular essay operating system.

## 1. Course Identity
- **Course Code:** ENG101_AMP_24FA
- **System Root:** `4_S0VRC3/INPD0000_instruction_pedagogy/`
- **Version:** v1a

## 2. Core Directories
| Folder (UID)        | Contents                       |
|---------------------|--------------------------------|
| `SYLL0000`          | Syllabus, expectations, calendar maps
| `ESSY0000`          | Essay units 1–5, UID tracked and ready
| `ZIPPED_EXPORTS`    | Exported units and submission bundles
| `UTIL0000`          | Utility scripts and future automation tools

## 3. Scripts and Commands
| Script             | Purpose                                |
|--------------------|----------------------------------------|
| `uid_check.py`     | Scan for duplicate UIDs                |
| `zip_unit.py`      | Package an essay folder for LMS/upload|
| `course_clone.py`  | Duplicate + version a full course      |
| `timeline_map.py`  | Display a calendar map weekly breakdown|

## 4. Deployment Checklist
- [x] All `UID_MAP.md` files present
- [x] All essay modules follow UID schema
- [x] Calendar maps aligned to module structure
- [x] All files Obsidian-ready and Markdown-based
- [x] Exports `.zip` and utility scripts included

## 5. UID System Logic
- Format: `AB-CD_12-34` (expanded), `ABCD1234` (condensed)
- Every folder, file, prompt, and script has a UID or prefix
- `00` used for system folders or general index files

## 6. Launch Notes
- Adjust calendar maps based on delivery mode (6w/8w/12w/16w)
- Use `README_DEPLOYMENT.md` to hand off system to a new instructor
- Zip individual units before uploading to LMS or printing

## 7. Next Steps
- Add instructor-specific `INSTRUCTOR_NOTES.md` per term
- Connect UID feedback comments to grading rubrics (future feature)
- Expand `UTIL0000` with Obsidian plugins or GUI interface

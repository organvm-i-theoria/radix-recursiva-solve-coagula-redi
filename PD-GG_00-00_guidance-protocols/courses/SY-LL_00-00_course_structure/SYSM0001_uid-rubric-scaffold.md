# SYSM0001_uid-rubric-scaffold

This is a UID-based semantic feedback scaffold. Each line item can be mapped to a specific UID (e.g., `CMCN_03-03`) and used to automate or structure grading feedback in Canvas, Obsidian, or PDF.

## Structure
| UID         | Category         | Criteria Description                        | Type         | Tag               |
|-------------|------------------|---------------------------------------------|--------------|-------------------|
| NRTV_01-03  | Thesis/Focus     | Strong emotional center in narrative        | High-Order   | `#focus`          |
| PRNS_02-02  | Logic/Flow       | Steps clearly ordered with transitions      | High-Order   | `#logic`          |
| CMCN_03-03  | Analysis/Insight | Thesis compares meaning, not just plot      | High-Order   | `#compare`        |
| ARRG_04-03  | Argument Quality | Counterargument is addressed and resolved   | High-Order   | `#argument`       |
| PFRT_05-03  | Reflection       | Revision is linked to specific UID feedback | Meta         | `#revision`       |

## Usage
- These entries can be linked in `REVISION_HISTORY.md` or comments in Canvas: “See UID `CMCN_03-03` for your revised insight claim.”
- You can build a dropdown menu in Canvas with these tags or use them as autofill with tools like TextExpander or PhraseExpress.
- In Obsidian, create a tag index using `#compare`, `#revision`, etc. for reference and back-linking.

## Feedback Tag Suggestions
- `#focus`, `#structure`, `#logic`, `#compare`, `#evidence`, `#voice`, `#clarity`, `#revision`, `#insight`, `#thesis`

## Future Tooling Ideas
- Script to auto-match `UID` to feedback templates
- GUI rubric builder for instructors with checkboxes + comment auto-insert
- UID crosswalk CSV for LMS import/export with numeric weighting

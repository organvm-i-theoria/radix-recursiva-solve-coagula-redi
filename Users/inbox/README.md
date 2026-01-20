<<<AI-Handoff:BEGIN::Agent=Codex::Task=InboxProtocol::Timestamp=2025-05-05T01:00:00Z>>>
# User Inbox Intake Protocol

This folder captures uploads, brainstorms, and early drafts before they are curated into the canonical knowledge base.

## Submission Checklist
1. **Filename Prefix**: Use `YYYYMMDD_topic_author` for chronological sorting.
2. **Metadata File**: Pair each asset with a `.meta.json` file describing origin, authorship, confidentiality, and review deadline.
3. **Classification Tags**: Reference `THREAD_PROJECT_CROSSWALK_TAGGED.md` to attach project and topic identifiers.
4. **Provenance Notes**: Document source systems, context, and transformation steps for transparency.

## Review Workflow
1. Intake agent triages new items within 24 hours and assigns reviewers.
2. Reviewers annotate decisions inside the metadata file (`status` field: Draft, In Review, Approved, Rejected).
3. Approved assets move to the appropriate repository folder, with links recorded in `vault_state.md`.
4. Rejected assets remain here with rationale for future reference.

## Automation Hooks
- Scheduled script `scripts/inbox_watcher.py` scans for new files and posts notifications to the coordination channel.
- Validation checks ensure metadata completeness prior to routing tasks.

## Privacy & Compliance
- Do not store credentials or personal data without encryption and explicit approval.
- Follow `SECURITY.md` guidelines for handling sensitive material.

<<<AI-Handoff:END>>>

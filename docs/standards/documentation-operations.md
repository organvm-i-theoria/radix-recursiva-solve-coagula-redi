---
title: Documentation Operations Standards
summary: Repeatable conventions for naming, metadata, and organisation that keep the knowledge base portable and easy to maintain.
tags:
  - governance
  - documentation
  - information-architecture
status: active
created: 2025-05-05
updated: 2025-05-05
---

# Documentation Operations Standards

The practices in this guide establish predictable patterns that make the repository navigable for new collaborators and resilient over time. They focus on conventions that are easy to teach, automate, and reuse across unrelated projects.

## Naming convention standard

- **Primary pattern:** Use lower-case `kebab-case` for every directory and file that will be committed to version control (for example, `project-overview.md`). Avoid brand names, numerals, or bespoke glyphs unless the content is inherently branded.
- **Semantic scope:** Begin file names with the most universal concept and narrow toward specificity (for example, `strategy-roadmap-retrospective.md`). This keeps alphabetical listings meaningful.
- **Temporal qualifiers:** When a date is required, append `-yyyy-mm-dd` in ISO 8601 format (`incident-report-2025-05-05.md`). Do not prefix with ambiguous numbering.
- **Cross references:** Refer to assets by their canonical path (for example, ``See `docs/guides/ai-helpers.md```), keeping references portable across tooling.
- **Exceptions:** Repository roots may keep `README.md` and `LICENSE` to align with community norms. All other Markdown files are expected to follow the pattern enforced by `scripts/metadata_guard.py`.

## Front matter and metadata requirements

Every Markdown document under `docs/` must begin with YAML front matter that provides the minimum metadata needed for cataloguing and search.

```yaml
---
title: Short, human-readable page title
summary: One-sentence overview that fits within 160 characters.
tags:
  - topic-one
  - topic-two
status: draft | active | deprecated | archived
created: 2025-05-05
updated: 2025-05-05
---
```

- **title** — A natural-language title; sentence case is preferred for readability.
- **summary** — Keep the summary concise to support listings and embed cards.
- **tags** — Provide at least one tag. Tags are lower-case `kebab-case` keywords.
- **status** — Use the controlled vocabulary: `draft`, `active`, `deprecated`, or `archived`.
- **created / updated** — Use ISO 8601 (`YYYY-MM-DD`). Update the `updated` value whenever substantive edits land.
- **Optional fields** — You may add keys such as `owner`, `version`, or `related` when additional structure helps discovery. Optional fields must remain lower-case `kebab-case` to stay machine-friendly.

## Organisational framework for storage

Adopt a layered structure that separates evergreen standards from topical content. The example below shows the recommended taxonomy.

```text
📦 repository-root/
├── docs/
│   ├── guides/              # How-to and onboarding material
│   ├── standards/           # Policies, conventions, and governance
│   └── templates/           # Reusable content scaffolds
├── projects/
│   └── {project-name}/
│       ├── briefs/
│       ├── decisions/
│       └── research/
├── archives/                # Immutable historical snapshots
├── scripts/                 # Automation and helper tooling
├── tests/                   # Automated regression coverage
└── .github/
    ├── workflows/           # CI/CD automation
    └── ISSUE_TEMPLATE/      # Optional issue templates
```

When introducing a new folder, document its purpose with a short `README.md` that follows the same front matter pattern. Archive deprecated material instead of deleting it to preserve decision history.

## GitHub and documentation best practices

1. **Branch hygiene** — Use topic branches named `feature/subject` or `chore/task`. Delete branches once merged.
2. **Commit format** — Follow `type: concise summary` where `type` is `feat`, `fix`, `docs`, `chore`, or `test`. Write body text when context is not obvious from the diff.
3. **Pull requests** — Include:
   - A summary of the change and its intent.
   - References to issues or discussion threads (`Resolves #123`).
   - Testing evidence (commands, screenshots, or reasoning when tests are impractical).
4. **Reviews** — Request at least one peer review. Allow automation (reviewdog, metadata guard, markdownlint) to run before requesting human review.
5. **Documentation upkeep** — When behaviour or workflows change, update the relevant guide in the same branch to keep docs and code in sync.
6. **Release notes** — Maintain a living `CHANGELOG.md` that follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) formatting for traceability.

## Repeatable process for new documentation

1. **Plan** — Place new content in the appropriate folder from the taxonomy above.
2. **Create** — Copy the front matter template from `docs/templates/front-matter-template.md` and populate required metadata.
3. **Draft** — Author the body content using markdownlint rules (`markdownlint-cli2` defines the style baseline).
4. **Validate** — Run `python scripts/metadata_guard.py docs` locally to ensure naming conventions and metadata pass.
5. **Review** — Open a pull request that references the change. The Knowledge Governance workflow will rerun the metadata guard and comment on violations.
6. **Publish** — Merge only after automated checks pass and reviewers approve. Update the `updated` metadata field on subsequent revisions.

Applying these steps consistently keeps the repository portable, searchable, and easy for future contributors to extend.

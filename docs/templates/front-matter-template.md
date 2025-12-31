---
title: Front Matter Template
summary: Copy-and-paste starter front matter for new documentation pages within the repository.
tags:
  - templates
  - documentation
status: active
created: 2025-05-05
updated: 2025-05-05
---

# Front Matter Template

Use this snippet as the opening block for any new Markdown document stored under `docs/`.

```yaml
---
title: Title in sentence case
summary: One-sentence summary that stays under 160 characters.
tags:
  - primary-topic
  - secondary-topic
status: draft
created: 2025-05-05
updated: 2025-05-05
---
```

## Field guidance

- Update `status` to `active` when the document becomes canonical, or `deprecated` / `archived` when superseded.
- Refresh the `updated` date whenever the content meaningfully changes.
- Add optional keys such as `owner`, `version`, or `related` when they aid discoverability, keeping names in lower-case `kebab-case`.

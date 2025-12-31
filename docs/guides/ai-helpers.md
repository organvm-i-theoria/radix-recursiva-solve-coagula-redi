---
title: AI Helpers and Code Review Automation
summary: Overview of the repository's free automation workflows for documentation linting and AI-assisted pull request feedback.
tags:
  - automation
  - documentation
  - github-actions
status: active
created: 2025-05-05
updated: 2025-05-05
---

# AI Helpers and Code Review Automation

This repository now includes GitHub Actions workflows that provide open-source automation for documentation quality checks and AI-assisted pull request reviews. The aim is to give collaborators free tooling that improves feedback loops without relying on paid APIs.

## Included workflows

### `Documentation Quality`
- **Location:** `.github/workflows/documentation-quality.yml`
- **What it does:**
  - Runs [`markdownlint-cli2`](https://github.com/DavidAnson/markdownlint-cli2) to enforce consistent Markdown style across the vault.
  - Uses the [`lychee`](https://github.com/lycheeverse/lychee) link checker with a shared configuration stored in `.github/lychee.toml`.
- **When it runs:** Automatically on pushes and pull requests that touch Markdown or CSV files, and it can also be triggered manually.

### `AI Assisted Review`
- **Location:** `.github/workflows/ai-review.yml`
- **What it does:**
  - Detects Markdown changes in a pull request and feeds the content through the open-source [`sumy`](https://github.com/miso-belica/sumy) library using an LSA summariser to produce a concise extractive summary.
  - Calculates readability metrics with [`textstat`](https://github.com/textstat/textstat), including flags for dense prose, long sentences, and missing sentence breaks that could hide comprehension issues.
  - Publishes the generated feedback as both an artifact (`ai_review_report.md`) and an automatic pull request comment, giving reviewers immediate context.
- **When it runs:** Each time a non-draft pull request is opened, updated, reopened, or marked ready for review.
- **Why it is free:** Everything runs inside GitHub-hosted runners against permissively licensed open-source packages. No API keys or paid services are required.

### `reviewdog Markdownlint`
- **Location:** `.github/workflows/reviewdog-markdown.yml`
- **What it does:** Runs [`markdownlint`](https://github.com/DavidAnson/markdownlint) through [`reviewdog`](https://github.com/reviewdog/reviewdog) so that violations appear as inline pull request comments instead of only failing the workflow. This gives contributors actionable feedback without leaving the PR conversation.
- **When it runs:** On every pull request that modifies Markdown files.
- **Why it is free:** Both markdownlint and reviewdog are open-source tools that execute inside the GitHub runner with no external dependencies.

### `Knowledge Governance`
- **Location:** `.github/workflows/knowledge-governance.yml`
- **What it does:** Executes `scripts/metadata_guard.py` to validate required front matter, metadata fields, and naming conventions for documentation housed in `docs/`.
- **When it runs:** On pushes and pull requests so structural regressions are caught before merge.
- **Why it is free:** The guard relies solely on the Python standard library and runs on GitHub-hosted infrastructure.

## Local usage

You can reproduce the AI helper locally by running:

```bash
python -m pip install --upgrade pip
pip install sumy==0.11.0 textstat==0.7.3
python scripts/ai_reviewer.py --base main --head HEAD
```

This generates `ai_review_report.md` with the same structure GitHub Actions produces.

## Extending the helpers

- To add new quality gates, extend the existing workflows with additional steps (for example, `vale` for prose linting or `typos` for spell checking). reviewdog also supports [many other linters](https://github.com/reviewdog/reviewdog#integrations) if you want inline feedback for different languages.
- The AI review script accepts extra file extensions via `--include`. For example, to analyse `.txt` and `.md` files, adjust the workflow command to `--include .md .txt`.
- The reviewer performs defensive checks for deleted/binary files and git diff failures, surfacing actionable diagnostics in the generated report instead of silently failing.
- If you prefer neural summarisation, swap the `sumy` dependency for a local HuggingFace model and update `scripts/ai_reviewer.py` accordingly. Keep in mind that larger models will increase runtime and download size.

## Complementary free services

You can pair the built-in automation with other no-cost services listed below to broaden coverage:

- **DeepSource** — enable at [deepsource.io](https://deepsource.io/) to receive static-analysis reports across multiple languages. It generates a `.deepsource.toml` configuration once the repository is connected.
- **CodeFactor** — connect the repository at [codefactor.io](https://www.codefactor.io/) for quick style and complexity checks. The service automatically reports issues on pull requests.
- **Danger** — the [Danger JS](https://danger.systems/js/) tooling can run custom rules on each diff. Add the OpenAI plugin only if you supply an API key; otherwise you still benefit from deterministic scripted checks.
- **Sorcery** — for Python-heavy projects, [Sorcery](https://sorcery.ai/) provides free refactor suggestions via its GitHub Action.

## Troubleshooting

- If the AI review step fails because dependencies are unavailable, re-run the workflow; GitHub's package cache usually resolves transient registry hiccups.
- Draft pull requests intentionally skip AI feedback to avoid noisy intermediate results. Mark them as ready for review when you want the helper to post comments.
- For private forks with restricted environments, vendor the `sumy` dependency or pin to a compatible Python version to ensure deterministic runs.
- If `punkt` tokenizer data is unavailable in CI, the AI summary falls back to a diagnostic message instead of failing. Install it via `python -m nltk.downloader punkt` when full summaries are required.

# Jules coordination helpers (repo-local)

This folder contains small scripts used to **reduce Jules branch proliferation** by:

- detecting when a task is already complete on `main`
- warning when branching from an old/stale base
- cleaning up stale bot-created branches by prefix + age

These scripts are safe to run locally and are designed to be used from GitHub Actions.

> Note: The long-term plan is to centralize these in the org-level `ivviiviivvi/.github` repo.
> This repo-local copy provides immediate relief and a working reference.

## Scripts

### `check_task_completion.py`
Detects if a task is already implemented.

- Default ref inspected: `origin/main`
- Exit code `1`: task detected (skip)
- Exit code `0`: task not detected (proceed)

Example:

- Check in the current checkout:
  - `python3 scripts/jules/check_task_completion.py --task-type bolt-optimize-containment --ref HEAD`
- Check against remote main:
  - `python3 scripts/jules/check_task_completion.py --task-type sentinel-path-traversal --ref origin/main`

To add new task signatures, extend `TASK_SIGNATURES` in the script.

### `check_base_freshness.py`
Checks whether a base ref is “fresh enough” to branch from.

- Default base ref: `origin/main`
- Default threshold: `--max-age-days 7`

Example:

- `python3 scripts/jules/check_base_freshness.py --base-ref origin/main --max-age-days 7`

### `cleanup_stale_branches.py`
Finds and deletes stale remote branches matching configured prefixes.

- Default prefixes: `bolt-`, `sentinel-`, `palette-`
- Default max age: `30` days
- `--dry-run` shows what would be deleted without deleting

Examples:

- Dry run (recommended first):
  - `python3 scripts/jules/cleanup_stale_branches.py --remote origin --max-age-days 30 --dry-run`
- Delete branches older than 120 days:
  - `python3 scripts/jules/cleanup_stale_branches.py --remote origin --max-age-days 120`
- Only delete palette branches older than 45 days:
  - `python3 scripts/jules/cleanup_stale_branches.py --remote origin --prefix palette- --max-age-days 45`

## Workflows

- `.github/workflows/jules-preflight.yml`
  - Manual workflow to evaluate whether a Jules run should proceed.
- `.github/workflows/jules-cleanup.yml`
  - Scheduled + manual cleanup of stale Jules branches.

## Safety notes

- Cleanup never deletes `main`/`master`.
- Prefer **dry runs** and create a backup tag before deletion.
- Use prefix filters to avoid deleting non-Jules branches.

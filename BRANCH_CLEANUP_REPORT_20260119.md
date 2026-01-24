# Branch Cleanup Report — 2026-01-19

This repo experienced rapid branch proliferation from `google-labs-jules[bot]`.

## Backup

Before deleting branches, a backup tag was created on `origin/main`:

- `pre-jules-branch-cleanup-20260119-213836`

## What was deleted

Deleted remote branches matching these prefixes:

- `bolt-`
- `sentinel-`
- `palette-`

A deletion list was generated locally for audit purposes:

- `branch_cleanup_delete_list_20260119-213841.txt` (177 branches)

## Counts

Before cleanup (remote):

- total deleted: **177**
- bolt: 59
- sentinel: 57
- palette: 61

After cleanup (remote):

- remaining `bolt-*|sentinel-*|palette-*`: **0**

## Prevention

To reduce recurrence, the repo now includes:

- `.github/workflows/jules-cleanup.yml` — scheduled/manual stale branch cleanup
- `.github/workflows/jules-preflight.yml` — manual preflight checks
- `.github/workflows/jules-branch-guard.yml` — auto-guard on branch creation (Jules bot only)


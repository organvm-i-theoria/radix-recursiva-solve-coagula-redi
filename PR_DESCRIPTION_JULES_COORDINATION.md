# 🤖 Add Jules Branch Coordination Infrastructure

## Problem Statement

Jules creates **hundreds of duplicate branches** solving the same problems:
- **solve-et-coagula**: 182 stale branches (36 sentinel, 28 bolt, 35 palette)
- **170 commits in 5 hours** - all solving same 3 tasks
- All branches based on **4-month-old commit** (Sept 2025)
- No coordination between Jules invocations

### Root Causes
1. **No memory** - Each Jules invocation starts fresh
2. **No branch awareness** - Can't see other Jules branches
3. **No convergence detection** - Doesn't know when task is done
4. **Stale base branch** - Always branches from old commits
5. **No cleanup** - Branches accumulate indefinitely

## Solution

Add **3-layer coordination system** to existing Jules infrastructure:

### 1️⃣ Prevention Layer (Week 1)
- ✅ Check if task already complete on main
- ✅ Limit to 5 branches per task type
- ✅ Ensure branching from fresh main (< 7 days)

### 2️⃣ Cleanup Layer (Week 2)
- ✅ Auto-delete branches older than 30 days
- ✅ Weekly scheduled cleanup
- ✅ Safe with backup tags

### 3️⃣ Tournament Layer (Future)
- 🔄 Compare competing branches
- 🔄 Auto-select winner
- 🔄 Delete inferior solutions

## Changes

### New Files

```
scripts/jules/
├── check_task_completion.py      # Detect if solution exists on main
├── check_base_freshness.py       # Ensure fresh base branch
├── branch_tournament.py          # Compare competing branches
├── cleanup_stale_branches.py     # Delete old branches
└── README.md                     # Documentation

.jules/
└── COORDINATION.md               # Branch coordination guide

.github/workflows/
├── jules-cleanup.yml             # Weekly cleanup workflow
└── jules-tournament.yml          # Branch competition (future)

workflow-templates/
└── jules-coordinator.yml         # For consumer repos

docs/jules/
├── BRANCH_MANAGEMENT.md          # How it works
├── INTEGRATION_GUIDE.md          # Adopting in repos
└── TROUBLESHOOTING.md            # Common issues
```

### Modified Files

- ✏️ `.github/workflows/jules.yml` - Add pre-flight checks

### File Details

#### `scripts/jules/check_task_completion.py`
```python
# Checks if task signature exists in codebase
# Patterns for: bolt-optimize, sentinel-path-traversal, palette-cards
# Returns exit code 1 if complete (skip Jules)
```

#### `.github/workflows/jules-cleanup.yml`
```yaml
# Runs weekly on Sunday 2am UTC
# Finds branches older than 30 days
# Creates backup tag before deletion
# Supports dry-run mode
```

#### `.jules/COORDINATION.md`
```markdown
# How coordination works
# Task signatures
# Manual operations
# Extending patterns
```

## Impact

### Before (Current State)
```
solve-et-coagula:
  - 182 branches (bolt-*, sentinel-*, palette-*)
  - Average age: 4 months
  - All solve same 3 problems
  - 170 commits in 5 hours (Jan 19)
```

### After (Expected)
```
All repos:
  - <20 active Jules branches
  - <5 branches per task type
  - Average age: <7 days
  - 95% reduction in duplicates
```

### Success Metrics
- **Branch count**: 182 → <20 per repo
- **Duplicate attempts**: 15 → <5 per task
- **Branch age**: 4 months → <7 days
- **Commit rate**: 170/5hrs → <10/day

## Testing Plan

### Phase 1: Trial Run (solve-et-coagula)
```bash
# 1. Backup current state
cd solve-et-coagula
git tag pre-jules-cleanup-20260119
git push origin pre-jules-cleanup-20260119

# 2. Dry run - see what would be deleted
gh workflow run jules-cleanup.yml -f dry_run=true -f max_age_days=120

# 3. Delete stale branches (Sept 2025 - Jan 2026)
gh workflow run jules-cleanup.yml -f dry_run=false -f max_age_days=120

# 4. Verify: should go from 182 → ~5 branches
git branch -r | grep -E 'bolt-|sentinel-|palette-' | wc -l
```

### Phase 2: Integrate Checks (Week 1)
```bash
# Test task completion detection
python scripts/jules/check_task_completion.py \
  --task-type bolt-optimize-containment \
  --repo-path /path/to/solve-et-coagula

# Test on new Jules invocation
# Should skip if solution already on main
```

### Phase 3: Roll Out (Week 2-3)
- Deploy to 2-3 other repos
- Monitor metrics
- Iterate based on feedback

## Rollback Plan

If issues occur:

```bash
# Restore deleted branches from backup tag
git checkout jules-cleanup-backup-20260119

# Disable cleanup workflow
gh workflow disable jules-cleanup.yml

# Revert jules.yml changes
git revert <commit-sha>
```

## Documentation

### For Repository Maintainers
- 📖 `docs/jules/INTEGRATION_GUIDE.md` - How to adopt
- 🔧 `.jules/COORDINATION.md` - How it works
- 🚨 `docs/jules/TROUBLESHOOTING.md` - Common issues

### For Jules Operators
- Pre-flight checks are automatic
- Comments explain why tasks are skipped
- Manual override: add `[force]` to comment

## Related Issues

- Addresses: #[issue] (Jules branch proliferation)
- Prevents: Duplicate PR creation
- Improves: Repository hygiene

## Dependencies

- **Python 3.x** (already required)
- **gh CLI** (already used in workflows)
- **jq** (already installed in runners)

## Breaking Changes

**None** - This is additive:
- Existing workflows continue to work
- New checks are non-blocking (warn only at first)
- Cleanup is opt-in via workflow_dispatch

## Security Considerations

✅ **Permissions**:
- Cleanup workflow requires `contents: write`
- Same permissions Jules already has

✅ **Safety**:
- Backup tags created before deletion
- Dry-run mode available
- 30-day grace period default

✅ **Audit Trail**:
- All deletions logged in workflow runs
- Backup tags track what was deleted
- Can restore from tags if needed

## Checklist

- [x] Code follows repository style guide
- [x] Documentation added/updated
- [x] Tested locally on solve-et-coagula
- [ ] Dry-run successful in CI
- [ ] Manual review by @[maintainer]
- [ ] Integration guide reviewed
- [ ] Ready for trial deployment

## Next Steps

1. **Review** this PR
2. **Test** cleanup on solve-et-coagula (trial)
3. **Monitor** results for 1 week
4. **Merge** to main if successful
5. **Deploy** to other repos using Jules
6. **Document** learnings

## Screenshots

### Before: 182 Branches
```
$ git branch -r | grep -E 'bolt-|sentinel-|palette-' | wc -l
182
```

### After Cleanup: ~5 Branches (Expected)
```
$ git branch -r | grep -E 'bolt-|sentinel-|palette-' | wc -l
5
```

### Task Completion Detection
```
$ python scripts/jules/check_task_completion.py --task-type bolt-optimize-containment
🔍 Checking for: Path caching optimization
✅ Task 'Path caching optimization' already complete
   Found in: experimental_habitat_implementation.py

🛑 STOP: Task already complete - skipping branch creation
```

---

**Questions?** See [docs/jules/TROUBLESHOOTING.md](docs/jules/TROUBLESHOOTING.md) or comment below.

**Ready to test?** Run cleanup trial on solve-et-coagula first.

# Jules Branch Coordination Integration Plan
**Target Repository**: `ivviiviivvi/.github`  
**Integration Date**: 2026-01-19  
**Purpose**: Add branch coordination layer to existing Jules infrastructure

---

## 🎯 Current State

The `.github` repository already has:
- ✅ `.jules/` directory (bolt.md, palette.md, sentinel.md)
- ✅ `jules.yml` workflow with deduplication
- ✅ `scripts/` directory with extensive automation
- ✅ `workflow-templates/` for reusable workflows
- ✅ `automation/` directory for tooling

**Missing**: Branch proliferation prevention (182 branches in solve-et-coagula)

---

## 📁 Proposed Directory Structure

```
ivviiviivvi/.github/
├── .jules/
│   ├── bolt.md                    # [EXISTS]
│   ├── palette.md                 # [EXISTS]
│   ├── sentinel.md                # [EXISTS]
│   └── COORDINATION.md            # [NEW] Branch coordination guide
│
├── scripts/
│   ├── jules/                     # [NEW] Jules-specific scripts
│   │   ├── check_task_completion.py
│   │   ├── check_base_freshness.py
│   │   ├── branch_tournament.py
│   │   ├── cleanup_stale_branches.py
│   │   └── README.md
│   │
│   ├── quota_manager.py           # [EXISTS]
│   └── ... (other scripts)
│
├── .github/workflows/
│   ├── jules.yml                  # [EXISTS - ENHANCE]
│   ├── jules-cleanup.yml          # [NEW] Stale branch cleanup
│   └── jules-tournament.yml       # [NEW] Branch competition
│
├── workflow-templates/
│   └── jules-coordinator.yml      # [NEW] For consumer repos
│
└── docs/
    └── jules/                     # [NEW] Jules documentation
        ├── BRANCH_MANAGEMENT.md
        ├── INTEGRATION_GUIDE.md
        └── TROUBLESHOOTING.md
```

---

## 🔧 File Changes

### 1. **ENHANCE**: `.github/workflows/jules.yml`

**Add before "Run Claude Code" step**:

```yaml
      - name: Check for duplicate branches
        id: branch_check
        run: |
          # Check if this task already has branches
          TASK_TYPE=$(echo "${{ github.event.comment.body || github.event.issue.body }}" | \
            grep -oE 'bolt-|sentinel-|palette-' | head -1)
          
          if [ -n "$TASK_TYPE" ]; then
            BRANCH_COUNT=$(gh api "repos/${{ github.repository }}/branches" --paginate | \
              jq "[.[] | select(.name | startswith(\"${TASK_TYPE}\"))] | length")
            
            echo "branch_count=$BRANCH_COUNT" >> $GITHUB_OUTPUT
            echo "task_type=$TASK_TYPE" >> $GITHUB_OUTPUT
            
            if [ "$BRANCH_COUNT" -gt 5 ]; then
              echo "⚠️ Already $BRANCH_COUNT branches for ${TASK_TYPE}"
              echo "should_skip=true" >> $GITHUB_OUTPUT
            else
              echo "should_skip=false" >> $GITHUB_OUTPUT
            fi
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Check if task complete on main
        if: steps.branch_check.outputs.should_skip != 'true'
        run: |
          python3 scripts/jules/check_task_completion.py \
            --task-type "${{ steps.branch_check.outputs.task_type }}" \
            --repo-path "."
```

### 2. **CREATE**: `scripts/jules/check_task_completion.py`

```python
#!/usr/bin/env python3
"""
Check if a Jules task is already complete on main branch.
Prevents creating duplicate branches when solution already exists.
"""
import argparse
import subprocess
import re
import sys
from pathlib import Path

# Task signatures - extend as needed
TASK_SIGNATURES = {
    'bolt-optimize-containment': {
        'files': ['experimental_habitat_implementation.py'],
        'patterns': [r'self\._full_path\s*=.*get_full_path\(\)'],
        'description': 'Path caching optimization'
    },
    'sentinel-path-traversal': {
        'files': ['experimental_habitat_implementation.py'],
        'patterns': [r'def _validate_experiment_name', r'\.\..*not allowed'],
        'description': 'Path traversal validation'
    },
    'palette-cli-cards': {
        'files': ['habitat_ux.py', 'habitat_manager.py'],
        'patterns': [r'def print_card', r'habitat_ux\.print_card'],
        'description': 'CLI card pattern'
    }
}

def check_task_complete(task_type: str, repo_path: Path, branch: str = 'main') -> bool:
    """Check if task signature exists in codebase"""
    # Fuzzy match task type
    matched_sig = None
    for sig_key in TASK_SIGNATURES:
        if sig_key in task_type:
            matched_sig = TASK_SIGNATURES[sig_key]
            break
    
    if not matched_sig:
        print(f"ℹ️  Unknown task type: {task_type}")
        return False
    
    print(f"🔍 Checking for: {matched_sig['description']}")
    
    for file_path in matched_sig['files']:
        try:
            # Try to read file from repo
            full_path = repo_path / file_path
            if not full_path.exists():
                continue
                
            content = full_path.read_text()
            
            # Check if all patterns exist
            matches = [
                re.search(pattern, content) 
                for pattern in matched_sig['patterns']
            ]
            
            if all(matches):
                print(f"✅ Task '{matched_sig['description']}' already complete")
                print(f"   Found in: {file_path}")
                return True
                
        except Exception as e:
            print(f"⚠️  Could not check {file_path}: {e}")
            continue
    
    print(f"❌ Task not complete")
    return False

def main():
    parser = argparse.ArgumentParser(
        description='Check if Jules task is already complete'
    )
    parser.add_argument('--task-type', required=True,
                       help='Task type (e.g., bolt-optimize-containment)')
    parser.add_argument('--repo-path', default='.',
                       help='Path to repository')
    parser.add_argument('--branch', default='main',
                       help='Branch to check (default: main)')
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if check_task_complete(args.task_type, repo_path, args.branch):
        print("\n🛑 STOP: Task already complete - skipping branch creation")
        sys.exit(1)  # Signal to skip Jules invocation
    else:
        print("\n✅ PROCEED: Task not complete - Jules should run")
        sys.exit(0)

if __name__ == '__main__':
    main()
```

### 3. **CREATE**: `.github/workflows/jules-cleanup.yml`

```yaml
name: Jules Branch Cleanup

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2am UTC
  workflow_dispatch:
    inputs:
      dry_run:
        description: 'Dry run (do not delete)'
        required: false
        default: 'true'
      max_age_days:
        description: 'Max age in days'
        required: false
        default: '30'

jobs:
  cleanup:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Backup current state
        run: |
          TAG="jules-cleanup-backup-$(date +%Y%m%d-%H%M%S)"
          git tag "$TAG"
          git push origin "$TAG"
          echo "✅ Created backup tag: $TAG"
      
      - name: Find stale branches
        id: find
        run: |
          MAX_AGE_DAYS="${{ github.event.inputs.max_age_days || '30' }}"
          CUTOFF_DATE=$(date -d "$MAX_AGE_DAYS days ago" +%s)
          
          echo "🔍 Finding branches older than $MAX_AGE_DAYS days..."
          
          STALE_BRANCHES=()
          
          git for-each-ref refs/remotes/origin --format='%(refname:short) %(committerdate:unix)' | \
            grep -E 'origin/(bolt-|sentinel-|palette-)' | \
            while read branch date; do
              if [ "$date" -lt "$CUTOFF_DATE" ]; then
                BRANCH_NAME="${branch#origin/}"
                AGE_DAYS=$(( ($(date +%s) - date) / 86400 ))
                echo "  - $BRANCH_NAME ($AGE_DAYS days old)"
                STALE_BRANCHES+=("$BRANCH_NAME")
              fi
            done
          
          echo "Found ${#STALE_BRANCHES[@]} stale branches"
          echo "count=${#STALE_BRANCHES[@]}" >> $GITHUB_OUTPUT
      
      - name: Delete stale branches
        if: github.event.inputs.dry_run != 'true'
        run: |
          git branch -r | grep -E 'origin/(bolt-|sentinel-|palette-)' | \
            sed 's|origin/||' | \
            xargs -I {} -P 5 sh -c 'echo "Deleting {}"; git push origin --delete {} 2>/dev/null || true'
          
          echo "✅ Cleanup complete!"
      
      - name: Dry run summary
        if: github.event.inputs.dry_run == 'true'
        run: |
          echo "🔍 DRY RUN - No branches deleted"
          echo "Found ${{ steps.find.outputs.count }} stale branches"
          echo "Run with dry_run=false to delete"
```

### 4. **CREATE**: `.jules/COORDINATION.md`

```markdown
# Jules Branch Coordination

**Problem**: Jules creates duplicate branches (182 in solve-et-coagula)  
**Solution**: Coordination layer prevents duplicates

## How It Works

1. **Task Completion Detection** - Check if main already has solution
2. **Branch Counting** - Limit to 5 attempts per task type
3. **Weekly Cleanup** - Auto-delete branches older than 30 days
4. **Tournament System** - Compare branches, keep winner

## For Jules Operators

Before creating branch, Jules now checks:
- ✅ Is solution already on main?
- ✅ Are there already 5+ branches for this task?
- ✅ Is base branch fresh (< 7 days old)?

If any check fails, Jules skips task and comments why.

## Extending Task Signatures

Edit `scripts/jules/check_task_completion.py`:

\`\`\`python
TASK_SIGNATURES['your-new-task'] = {
    'files': ['path/to/file.py'],
    'patterns': [r'regex_pattern_to_find'],
    'description': 'What this task does'
}
\`\`\`

## Manual Cleanup

\`\`\`bash
# List stale branches
gh workflow run jules-cleanup.yml -f dry_run=true

# Delete stale branches
gh workflow run jules-cleanup.yml -f dry_run=false
\`\`\`
```

---

## 🚀 Integration Steps

### For .github Repository

1. **Create branch**: `infra/jules-branch-coordination`
2. **Add scripts**: Copy from JULES_WORKFLOW_FIX_PROPOSAL.md
3. **Enhance workflow**: Update jules.yml with checks
4. **Add cleanup**: Create jules-cleanup.yml
5. **Document**: Add .jules/COORDINATION.md
6. **Test**: Run on solve-et-coagula (has 182 branches)
7. **Deploy**: Merge to main

### For Consumer Repos (solve-et-coagula, etc.)

**Option A: Automatic (from .github)** 
- Run `gh workflow run deploy-jules-coordination.yml`
- Creates PR in each repo

**Option B: Manual**
- Copy `.github/workflows/jules-coordinator.yml` from templates
- Update jules invocation to use coordinator

---

## 📊 Success Metrics

**Before**:
- 182 branches in solve-et-coagula
- 170 commits in 5 hours
- All based on 4-month-old commit

**After (Target)**:
- <20 active branches per repo
- <5 branches per task type
- All branches < 30 days old
- 95% reduction in duplicate work

---

## 🔗 Related Files

- Original proposal: `solve-et-coagula/JULES_WORKFLOW_FIX_PROPOSAL.md`
- Migration plan: `solve-et-coagula/JULES_INFRASTRUCTURE_MIGRATION_PLAN.md`
- Task deduplication: `.github/scripts/task_deduplicator.py` (already exists)

---

**Next**: Create PR to .github repository with these changes

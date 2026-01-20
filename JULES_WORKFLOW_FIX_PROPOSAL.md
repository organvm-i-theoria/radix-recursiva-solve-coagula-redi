# Jules Workflow Fix Proposal
**Status**: Draft  
**Date**: 2026-01-19  
**Problem**: Jules creates hundreds of duplicate branches solving the same tasks  
**Impact**: 182 stale branches, manual merge harvesting, repository pollution  

---

## 🔴 Problem Statement

### Current Behavior
Jules (google-labs-jules[bot]) operates in a **fire-and-forget pattern**:

1. Receives task (e.g., "optimize path performance")
2. Creates branch from stale base commit (Sept 2025)
3. Implements solution without checking if it already exists
4. Pushes branch with random ID suffix
5. **Never checks if task is complete**
6. **Repeats indefinitely** - 170 commits in 5 hours observed

### Evidence from solve-et-coagula
```
182 total branches:
- 36 sentinel-path-traversal-fix-* (same security fix)
- 28 bolt-optimize-containment-path-* (same optimization)
- 35 palette-cli-cards-* (same UX improvement)
- All based on 4-month-old commit (3281155)
- Main already merged best implementations
```

### Root Causes
1. **No state persistence** between Jules invocations
2. **No branch awareness** - can't see other Jules branches
3. **No convergence detection** - doesn't know when task is done
4. **Stale base branch** - always branches from old commit
5. **No cleanup mechanism** - branches accumulate forever

---

## 🎯 Solution Architecture

### Phase 1: Detection & Prevention (Immediate)

#### 1.1 Branch Awareness System
**Goal**: Jules checks existing branches before creating new ones

```yaml
# .github/workflows/jules-coordinator.yml
name: Jules Coordinator

on:
  workflow_dispatch:
    inputs:
      task_type:
        description: 'Task category (bolt/sentinel/palette/feat)'
        required: true
      task_description:
        description: 'What needs to be done'
        required: true

jobs:
  check-existing:
    runs-on: ubuntu-latest
    outputs:
      should_proceed: ${{ steps.check.outputs.proceed }}
      existing_branches: ${{ steps.check.outputs.branches }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Check for existing solutions
        id: check
        run: |
          # Check if main already has this fix
          TASK_TYPE="${{ inputs.task_type }}"
          
          # Search for branches working on same task
          EXISTING=$(git branch -r | grep "origin/${TASK_TYPE}-" | wc -l)
          
          echo "branches=${EXISTING}" >> $GITHUB_OUTPUT
          
          if [ $EXISTING -gt 5 ]; then
            echo "proceed=false" >> $GITHUB_OUTPUT
            echo "⚠️ Already ${EXISTING} branches for ${TASK_TYPE}"
          else
            echo "proceed=true" >> $GITHUB_OUTPUT
          fi
      
      - name: Check if already in main
        run: |
          python scripts/check_task_completion.py \
            --task-type "${{ inputs.task_type }}" \
            --description "${{ inputs.task_description }}"
```

#### 1.2 Task Completion Detector
**Goal**: Detect if main already has the solution

```python
# scripts/check_task_completion.py
"""
Checks if a task is already complete on main branch
"""
import argparse
import subprocess
import sys

TASK_SIGNATURES = {
    'bolt-optimize-containment-path': {
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

def check_task_complete(task_type, branch='main'):
    """Check if task signature exists in codebase"""
    if task_type not in TASK_SIGNATURES:
        return False
    
    signature = TASK_SIGNATURES[task_type]
    
    for file_path in signature['files']:
        try:
            content = subprocess.check_output(
                ['git', 'show', f'{branch}:{file_path}'],
                text=True, stderr=subprocess.DEVNULL
            )
            
            # Check if all patterns exist
            import re
            matches = [
                re.search(pattern, content) 
                for pattern in signature['patterns']
            ]
            
            if all(matches):
                print(f"✅ Task '{signature['description']}' already complete on {branch}")
                return True
                
        except subprocess.CalledProcessError:
            continue
    
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-type', required=True)
    parser.add_argument('--description', required=False)
    args = parser.parse_args()
    
    if check_task_complete(args.task_type):
        print("🛑 STOP: Task already complete")
        sys.exit(1)  # Signal to skip Jules invocation
    else:
        print("✅ PROCEED: Task not complete")
        sys.exit(0)
```

#### 1.3 Base Branch Freshness Check
**Goal**: Prevent branching from stale commits

```python
# scripts/check_base_freshness.py
"""
Ensures Jules branches from recent main, not ancient commits
"""
import subprocess
import sys
from datetime import datetime, timedelta

def get_commit_age(commit_sha):
    """Get age of commit in days"""
    timestamp = subprocess.check_output(
        ['git', 'show', '-s', '--format=%ct', commit_sha],
        text=True
    ).strip()
    
    commit_date = datetime.fromtimestamp(int(timestamp))
    age = datetime.now() - commit_date
    return age.days

def main():
    # Get current base commit
    base_sha = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'],
        text=True
    ).strip()
    
    age_days = get_commit_age(base_sha)
    
    if age_days > 7:
        print(f"❌ Base commit is {age_days} days old")
        print("🔄 Fetching latest main...")
        subprocess.run(['git', 'fetch', 'origin', 'main'])
        subprocess.run(['git', 'reset', '--hard', 'origin/main'])
        print("✅ Reset to fresh main")
    else:
        print(f"✅ Base commit is {age_days} days old (acceptable)")
    
    sys.exit(0)

if __name__ == '__main__':
    main()
```

---

### Phase 2: Convergence & Cleanup (Short-term)

#### 2.1 Branch Tournament System
**Goal**: When multiple solutions exist, automatically test and select winner

```python
# scripts/branch_tournament.py
"""
Compares multiple branches solving same task, picks winner
"""
import subprocess
import json
from typing import List, Dict

def run_tests_on_branch(branch_name: str) -> Dict:
    """Checkout branch, run tests, collect metrics"""
    subprocess.run(['git', 'checkout', branch_name], check=True)
    
    # Run tests
    test_result = subprocess.run(
        ['pytest', '-v', '--tb=short'],
        capture_output=True, text=True
    )
    
    # Run performance benchmarks
    perf_result = subprocess.run(
        ['python', 'scripts/benchmark.py'],
        capture_output=True, text=True
    )
    
    return {
        'branch': branch_name,
        'tests_passed': test_result.returncode == 0,
        'test_output': test_result.stdout,
        'performance': parse_benchmark(perf_result.stdout)
    }

def select_winner(results: List[Dict]) -> str:
    """Pick best branch based on tests + performance"""
    
    # Filter to passing tests only
    passing = [r for r in results if r['tests_passed']]
    
    if not passing:
        return None
    
    # Sort by performance
    winner = max(passing, key=lambda r: r['performance']['score'])
    
    return winner['branch']

def main():
    # Find all branches of same category
    branches = subprocess.check_output(
        ['git', 'branch', '-r', '--list', 'origin/bolt-optimize-containment-path-*'],
        text=True
    ).strip().split('\n')
    
    print(f"🏆 Running tournament on {len(branches)} branches...")
    
    results = []
    for branch in branches[:10]:  # Limit to 10 for speed
        branch = branch.strip()
        print(f"  Testing {branch}...")
        result = run_tests_on_branch(branch)
        results.append(result)
    
    winner = select_winner(results)
    
    if winner:
        print(f"\n✅ Winner: {winner}")
        print(f"   Tests passed: ✓")
        print(f"   Performance: {results[0]['performance']['score']}")
        
        # Tag winner for manual review
        subprocess.run(['git', 'tag', f'tournament-winner-{datetime.now().strftime("%Y%m%d")}', winner])
    
    # Delete losers
    losers = [r['branch'] for r in results if r['branch'] != winner]
    print(f"\n🗑️  Deleting {len(losers)} inferior branches...")
    for branch in losers:
        subprocess.run(['git', 'push', 'origin', '--delete', branch.replace('origin/', '')])

if __name__ == '__main__':
    main()
```

#### 2.2 Automatic Stale Branch Cleanup
**Goal**: Delete branches that haven't been touched in 30 days

```yaml
# .github/workflows/cleanup-stale-branches.yml
name: Cleanup Stale Branches

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2am
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Delete stale Jules branches
        run: |
          # Find branches older than 30 days
          CUTOFF_DATE=$(date -d '30 days ago' +%s)
          
          git branch -r --format='%(refname:short) %(committerdate:unix)' | 
            grep 'origin/bolt-\|origin/sentinel-\|origin/palette-' |
            while read branch date; do
              if [ "$date" -lt "$CUTOFF_DATE" ]; then
                echo "🗑️  Deleting stale: $branch ($(( ($(date +%s) - date) / 86400 )) days old)"
                git push origin --delete "${branch#origin/}" || true
              fi
            done
      
      - name: Report cleanup
        run: |
          REMAINING=$(git branch -r | grep -E 'bolt-|sentinel-|palette-' | wc -l)
          echo "✅ Cleanup complete. ${REMAINING} branches remaining."
```

---

### Phase 3: Jules Coordination Layer (Long-term)

#### 3.1 Shared State Service
**Goal**: All Jules instances share knowledge

```yaml
# Architecture: Redis or GitHub Actions cache for state

shared_state:
  active_tasks:
    bolt-optimize-containment:
      status: in_progress
      branches: [bolt-optimize-123, bolt-optimize-456]
      started: 2026-01-19T12:00:00Z
      attempts: 15
      last_success: bolt-optimize-123
    
    sentinel-path-traversal:
      status: complete
      merged_to_main: 2026-01-18T19:00:00Z
      solution_commit: de252f3
      should_skip: true
```

#### 3.2 Jules Workflow Wrapper
**Goal**: Every Jules invocation goes through coordinator

```yaml
# .github/workflows/jules-wrapper.yml
name: Jules Coordinated Workflow

on:
  workflow_dispatch:
    inputs:
      task: 
        required: true

jobs:
  coordinate:
    runs-on: ubuntu-latest
    steps:
      - name: Check state
        id: state
        run: |
          # Query shared state
          TASK_STATE=$(curl -s "$STATE_API/task/${{ inputs.task }}")
          
          # Parse state
          STATUS=$(echo "$TASK_STATE" | jq -r '.status')
          ATTEMPTS=$(echo "$TASK_STATE" | jq -r '.attempts')
          
          if [ "$STATUS" = "complete" ]; then
            echo "skip=true" >> $GITHUB_OUTPUT
            echo "reason=already_complete" >> $GITHUB_OUTPUT
            exit 0
          fi
          
          if [ "$ATTEMPTS" -gt 10 ]; then
            echo "skip=true" >> $GITHUB_OUTPUT
            echo "reason=too_many_attempts" >> $GITHUB_OUTPUT
            exit 0
          fi
          
          echo "skip=false" >> $GITHUB_OUTPUT
      
      - name: Invoke Jules
        if: steps.state.outputs.skip == 'false'
        run: |
          # Update state: increment attempts
          curl -X POST "$STATE_API/task/${{ inputs.task }}/attempt"
          
          # Run actual Jules workflow
          gh workflow run jules-actual.yml -f task="${{ inputs.task }}"
      
      - name: Record result
        if: always()
        run: |
          # Update state with result
          curl -X POST "$STATE_API/task/${{ inputs.task }}/complete"
```

---

## 📋 Implementation Roadmap

### Week 1: Immediate Relief
- [ ] Deploy stale branch cleanup workflow (2.2)
- [ ] Run initial cleanup: delete 182 stale branches
- [ ] Document current state in BRANCH_AUDIT.md
- [ ] Tag main with `pre-cleanup-backup`

### Week 2: Prevention Layer
- [ ] Implement base branch freshness check (1.3)
- [ ] Add task completion detector (1.2)
- [ ] Update CI to run checks before Jules invocation
- [ ] Test on 5 new tasks

### Week 3-4: Convergence System
- [ ] Build branch tournament script (2.1)
- [ ] Run tournament on existing branch categories
- [ ] Automate weekly tournaments
- [ ] Set up metrics dashboard

### Month 2-3: Coordination Layer (Optional)
- [ ] Design shared state service architecture
- [ ] Implement Jules coordination API
- [ ] Migrate workflows to use coordinator
- [ ] Deploy to production

---

## 🎯 Success Metrics

### Quantitative
- **Branch count**: 182 → <20 within 30 days
- **Duplicate attempts**: 15 per task → <3 per task
- **Branch age**: Average 4 months → <7 days
- **Merge rate**: Manual → 80% auto-converged

### Qualitative
- Jules creates branch only when needed
- Duplicate solutions auto-resolved
- Main stays fresh with best implementations
- Repository stays clean and navigable

---

## 🚨 Risk Mitigation

### Risk: Accidental deletion of valuable work
**Mitigation**: 
- Tag all branches before deletion
- 30-day grace period
- Manual review of tournament winners

### Risk: False positives on "task complete"
**Mitigation**:
- Conservative pattern matching
- Manual override capability
- Log all skip decisions

### Risk: Coordination layer downtime
**Mitigation**:
- Degraded mode: Jules works without coordination
- Local state fallback
- Health checks and alerts

---

## 💡 Recommendations

### For This Repository (solve-et-coagula)
1. **Immediate**: Run cleanup, delete 182 stale branches
2. **This week**: Deploy freshness + completion checks
3. **Document**: What main already has (CURRENT_IMPLEMENTATION.md)

### For Jules Product Team
1. **Core fix**: Add branch awareness to Jules agent
2. **Architecture**: Consider coordination layer in Jules service
3. **Defaults**: Make freshness checks mandatory
4. **UI**: Show "task already complete" in Jules dashboard

### For Other Repositories Using Jules
1. **Audit**: Check for same branch proliferation pattern
2. **Deploy**: Use this cleanup workflow across all repos
3. **Educate**: Train teams on merge harvesting vs auto-merge

---

## 📚 Appendix

### A. Cleanup Script (Safe Execution)
```bash
#!/bin/bash
# cleanup_jules_branches.sh

set -e

echo "🔍 Analyzing Jules branches..."

# Backup: tag current state
git tag "pre-jules-cleanup-$(date +%Y%m%d)" main
git push origin "pre-jules-cleanup-$(date +%Y%m%d)"

# Count branches
BOLT_COUNT=$(git branch -r | grep -c 'origin/bolt-' || true)
SENTINEL_COUNT=$(git branch -r | grep -c 'origin/sentinel-' || true)
PALETTE_COUNT=$(git branch -r | grep -c 'origin/palette-' || true)

echo "Found:"
echo "  - $BOLT_COUNT bolt branches"
echo "  - $SENTINEL_COUNT sentinel branches"
echo "  - $PALETTE_COUNT palette branches"

read -p "Proceed with deletion? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
  echo "Aborted."
  exit 0
fi

# Delete in batches
echo "🗑️  Deleting branches..."

for category in bolt sentinel palette; do
  git branch -r | grep "origin/${category}-" | sed 's|origin/||' | \
    xargs -I {} -P 5 sh -c 'echo "Deleting {}"; git push origin --delete {} 2>/dev/null || true'
done

echo "✅ Cleanup complete!"
git branch -r | wc -l | xargs echo "Remaining branches:"
```

### B. Detection Patterns Reference
```python
# Extend TASK_SIGNATURES in check_task_completion.py

TASK_SIGNATURES = {
    'bolt-regex-optimization': {
        'files': ['experimental_habitat_implementation.py'],
        'patterns': [r're\.compile.*VALIDATION'],
        'description': 'Regex pre-compilation'
    },
    'sentinel-ansi-injection': {
        'files': ['habitat_ux.py'],
        'patterns': [r'def.*sanitize', r'ANSI.*strip'],
        'description': 'ANSI sanitization'
    },
    # ... add more as discovered
}
```

---

**End of Proposal**

**Next Steps**: Review → Approve → Deploy Phase 1 (cleanup) → Monitor → Iterate

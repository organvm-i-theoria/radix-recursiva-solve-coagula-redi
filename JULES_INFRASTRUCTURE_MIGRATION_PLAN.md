# Jules Infrastructure Migration Plan
**Target**: Move Jules coordination to `ivviiviivvi/.github` repository  
**Date**: 2026-01-19  
**Reason**: Centralize workflow tooling for all repositories using Jules

---

## 🎯 Why Centralize in `.github` Repository?

### Current Problem
- Jules workflow fixes duplicated across every repo
- Each repo maintains own cleanup scripts
- No shared state between repos
- Updates require changing 10+ repositories

### Benefits of `.github` Repository
✅ **Reusable workflows** - One workflow, all repos  
✅ **Organization defaults** - Apply to all repos automatically  
✅ **Centralized maintenance** - Update once, fix everywhere  
✅ **Shared state** - Cross-repo coordination possible  
✅ **GitHub convention** - Standard practice for org-level config

---

## 📂 Proposed Repository Structure

```
ivviiviivvi/.github/
├── README.md
├── workflow-templates/                    # Reusable workflow templates
│   ├── jules-coordinator.yml             # Main coordination workflow
│   ├── jules-cleanup.yml                 # Stale branch cleanup
│   ├── jules-tournament.yml              # Branch winner selection
│   └── jules-task-check.yml              # Task completion detector
│
├── scripts/                               # Shared scripts
│   ├── jules/
│   │   ├── check_task_completion.py      # Detect if task done
│   │   ├── check_base_freshness.py       # Ensure fresh base
│   │   ├── branch_tournament.py          # Run competitions
│   │   ├── cleanup_stale_branches.py     # Delete old branches
│   │   └── shared_state.py               # State coordination API
│   │
│   └── common/
│       ├── git_utils.py                   # Git helper functions
│       └── metrics.py                     # Telemetry collection
│
├── .github/
│   └── workflows/
│       ├── deploy-to-repos.yml           # Push updates to consumer repos
│       └── test-workflows.yml            # Test workflow changes
│
└── docs/
    ├── JULES_COORDINATION.md             # How coordination works
    ├── INTEGRATION_GUIDE.md              # How to adopt in your repo
    └── TROUBLESHOOTING.md                # Common issues
```

---

## 🔧 Migration Steps

### Phase 1: Create `.github` Repository (1 hour)

```bash
# Create the special .github repository
gh repo create ivviiviivvi/.github --public --description "Organization-wide GitHub configuration and Jules coordination"

# Clone and set up structure
git clone https://github.com/ivviiviivvi/.github
cd .github

# Create directory structure
mkdir -p workflow-templates scripts/jules scripts/common docs .github/workflows

# Initialize README
cat > README.md << 'EOF'
# ivviiviivvi/.github

Organization-wide GitHub configuration and Jules AI coordination infrastructure.

## What's Here

- **workflow-templates/**: Reusable GitHub Actions workflows
- **scripts/jules/**: Jules coordination and cleanup scripts
- **docs/**: Integration guides and documentation

## For Repository Maintainers

To adopt Jules coordination in your repo:

1. Copy workflow templates from `workflow-templates/` to your `.github/workflows/`
2. Follow `docs/INTEGRATION_GUIDE.md`
3. Run initial cleanup: `scripts/jules/cleanup_stale_branches.py`

## Components

### Jules Coordinator
Prevents duplicate branch creation by checking:
- Existing branches for same task
- Task completion status on main
- Base branch freshness

### Branch Tournament
Automatically tests competing solutions and selects winner.

### Stale Branch Cleanup
Weekly automated cleanup of branches older than 30 days.
EOF

git add README.md
git commit -m "Initial .github repository structure"
git push
```

### Phase 2: Migrate Scripts (2 hours)

**Copy from solve-et-coagula proposal to .github repo:**

```bash
# In .github repo
cd scripts/jules/

# Copy scripts (create these based on JULES_WORKFLOW_FIX_PROPOSAL.md)
# - check_task_completion.py
# - check_base_freshness.py  
# - branch_tournament.py
# - cleanup_stale_branches.py

# Make them organization-agnostic (accept repo as parameter)
```

**Key Change**: Scripts should accept `--repo` parameter:

```python
# OLD (repo-specific):
def check_task_complete(task_type, branch='main'):
    content = subprocess.check_output(['git', 'show', f'{branch}:file.py'])
    
# NEW (repo-agnostic):
def check_task_complete(task_type, repo_path, branch='main'):
    content = subprocess.check_output(
        ['git', 'show', f'{branch}:file.py'],
        cwd=repo_path
    )
```

### Phase 3: Create Reusable Workflows (3 hours)

**Example: workflow-templates/jules-coordinator.yml**

```yaml
# This workflow can be called by any repository
name: Jules Coordinator (Reusable)

on:
  workflow_call:
    inputs:
      task_type:
        required: true
        type: string
      task_description:
        required: true
        type: string
      repository:
        required: true
        type: string
    outputs:
      should_proceed:
        description: "Whether Jules should run"
        value: ${{ jobs.check.outputs.proceed }}

jobs:
  check:
    runs-on: ubuntu-latest
    outputs:
      proceed: ${{ steps.check.outputs.proceed }}
    steps:
      - name: Checkout target repo
        uses: actions/checkout@v4
        with:
          repository: ${{ inputs.repository }}
          fetch-depth: 0
      
      - name: Checkout .github scripts
        uses: actions/checkout@v4
        with:
          repository: ivviiviivvi/.github
          path: .github-org
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Check task completion
        id: check
        run: |
          python .github-org/scripts/jules/check_task_completion.py \
            --task-type "${{ inputs.task_type }}" \
            --repo-path "." \
            --description "${{ inputs.task_description }}"
          
          echo "proceed=$?" >> $GITHUB_OUTPUT
      
      - name: Check base freshness
        if: steps.check.outputs.proceed == '0'
        run: |
          python .github-org/scripts/jules/check_base_freshness.py \
            --repo-path "."
```

### Phase 4: Consumer Repo Integration (Per Repo, 30 min each)

**In solve-et-coagula/.github/workflows/jules-wrapped.yml:**

```yaml
name: Jules Wrapped (Uses Org Coordination)

on:
  workflow_dispatch:
    inputs:
      task:
        required: true
        description: 'Task for Jules to perform'

jobs:
  coordinate:
    uses: ivviiviivvi/.github/.github/workflows/jules-coordinator.yml@main
    with:
      task_type: ${{ github.event.inputs.task }}
      task_description: ${{ github.event.inputs.task }}
      repository: ${{ github.repository }}
  
  run-jules:
    needs: coordinate
    if: needs.coordinate.outputs.should_proceed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Jules
        run: |
          # Your existing Jules invocation
          echo "Running Jules on task: ${{ github.event.inputs.task }}"
```

### Phase 5: Deploy Cleanup Workflow (1 hour)

**In .github/workflows/deploy-to-repos.yml:**

```yaml
name: Deploy Jules Infrastructure to Repos

on:
  workflow_dispatch:
    inputs:
      target_repos:
        description: 'Repos to update (comma-separated, or "all")'
        required: true
        default: 'all'

jobs:
  deploy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        repo:
          - solve-et-coagula
          # Add other repos using Jules
    steps:
      - name: Checkout .github
        uses: actions/checkout@v4
      
      - name: Deploy to ${{ matrix.repo }}
        env:
          GH_TOKEN: ${{ secrets.ORG_PAT }}
        run: |
          # Clone target repo
          git clone "https://github.com/ivviiviivvi/${{ matrix.repo }}"
          cd "${{ matrix.repo }}"
          
          # Create integration branch
          git checkout -b "infra/jules-coordination"
          
          # Copy workflow template
          mkdir -p .github/workflows
          cp ../workflow-templates/jules-coordinator.yml \
             .github/workflows/jules-coordinator.yml
          
          # Commit and push
          git add .github/workflows/jules-coordinator.yml
          git commit -m "feat: integrate Jules coordination from .github repo"
          git push origin infra/jules-coordination
          
          # Create PR
          gh pr create \
            --title "Integrate Jules coordination infrastructure" \
            --body "Adopts centralized Jules coordination from ivviiviivvi/.github" \
            --base main \
            --head infra/jules-coordination
```

---

## 📋 Repository-by-Repository Rollout

### Priority 1: solve-et-coagula (This Repo)
**Status**: Has 182 stale branches - needs immediate cleanup  
**Actions**:
1. Run cleanup from .github scripts
2. Integrate coordinator workflow
3. Test tournament on remaining branches
4. **Timeline**: This week

### Priority 2: Other Repos with Jules
**Discovery needed**: Run audit across org

```bash
# Find all repos with Jules branches
gh repo list ivviiviivvi --limit 100 --json name | \
  jq -r '.[].name' | \
  while read repo; do
    count=$(gh api "repos/ivviiviivvi/$repo/branches" | \
            jq '[.[] | select(.name | test("bolt-|sentinel-|palette-"))] | length')
    if [ "$count" -gt 10 ]; then
      echo "$repo: $count Jules branches"
    fi
  done
```

### Priority 3: Documentation
- Integration guide for new repos
- Troubleshooting common issues
- Metrics dashboard

---

## 🎯 Success Criteria

### Organization Level
- [ ] .github repository created and populated
- [ ] Reusable workflows tested
- [ ] Scripts work across multiple repos
- [ ] Documentation complete

### Per Repository
- [ ] Integrated coordinator workflow
- [ ] Stale branches cleaned (182 → <20)
- [ ] No duplicate branch creation
- [ ] Team trained on new workflows

### Long-term
- [ ] Jules creates <5 branches per task
- [ ] Average branch age <7 days
- [ ] 80% of branches auto-converged
- [ ] Cross-repo state coordination working

---

## 🚀 Quick Start (Right Now)

```bash
# 1. Create .github repository
gh repo create ivviiviivvi/.github --public

# 2. Move JULES_WORKFLOW_FIX_PROPOSAL.md there
mv JULES_WORKFLOW_FIX_PROPOSAL.md ../temp/

# 3. Clone and set up
git clone https://github.com/ivviiviivvi/.github
cd .github
mkdir -p workflow-templates scripts/jules docs

# 4. Move proposal and extract components
mv ../temp/JULES_WORKFLOW_FIX_PROPOSAL.md docs/

# 5. Extract scripts from proposal into scripts/jules/
# (manual extraction from proposal code blocks)

# 6. Create README and push
git add .
git commit -m "Initial Jules coordination infrastructure"
git push

# 7. Return to solve-et-coagula and integrate
cd ../solve-et-coagula
# Create integration workflow that uses .github repo
```

---

## 📞 Next Steps

### Immediate (Today)
1. **Create** `ivviiviivvi/.github` repository
2. **Move** this proposal and fix scripts there
3. **Test** cleanup script on solve-et-coagula
4. **Document** integration guide

### This Week
5. **Integrate** coordinator in solve-et-coagula
6. **Run** initial cleanup (delete 182 branches)
7. **Audit** other repos for Jules branch pollution
8. **Deploy** to 2-3 other repos as proof of concept

### This Month
9. **Roll out** to all repos using Jules
10. **Monitor** metrics and effectiveness
11. **Iterate** on coordination layer
12. **Train** team on new workflows

---

**Key Decision**: Should we create `.github` repo now, or test locally first?

**Recommendation**: Create `.github` repo immediately. It's the standard pattern, and testing can happen there with workflow_dispatch triggers before rolling out to consumer repos.

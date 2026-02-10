---
uniqueID: "04"
title: 4_S0VRC3
tags:
  - protocol
  - template
  - digest
  - system
  - thread
---

[![ORGAN-I: Theory](https://img.shields.io/badge/ORGAN--I-Theory-1a237e?style=flat-square)](https://github.com/organvm-i-theoria)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-3776ab?style=flat-square&logo=python&logoColor=white)]()
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success?style=flat-square)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)]()
[![Status: Active](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)]()

# Radix Recursiva: Solve, Coagula, Redi

**A recursive generative operating system that unifies knowledge architecture, symbolic computation, and experimental containment into a single self-documenting vault — where the specification implements itself and naming conventions encode ontological meaning.**

The title is an alchemical formula. *Solve* — dissolve the existing structure, break apart assumptions and inherited categories. *Coagula* — recompose what was dissolved into new, more coherent form. *Redi* — return to the beginning, carrying the transformation forward into the next cycle. This is not decoration. It is the operating logic: every document, every experiment, every naming convention in this system passes through dissolution, recomposition, and recursive return. The repository name *is* the algorithm.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Core Concepts](#core-concepts)
  - [RE:GE:OS — Recursive Generative Operating System](#regeos--recursive-generative-operating-system)
  - [The Experimental Habitat System](#the-experimental-habitat-system)
  - [Symbolic UID Naming Convention](#symbolic-uid-naming-convention)
  - [The 22 Organizational Bodies](#the-22-organizational-bodies)
  - [Obsidian Knowledge Vault Integration](#obsidian-knowledge-vault-integration)
- [Architecture](#architecture)
  - [Directory Ontology](#directory-ontology)
  - [Python Package Structure](#python-package-structure)
  - [Data Flow: Solve, Coagula, Redi in Practice](#data-flow-solve-coagula-redi-in-practice)
- [Installation and Usage](#installation-and-usage)
- [Examples](#examples)
- [Vault Utilities and Automation](#vault-utilities-and-automation)
- [CI/CD and Governance Workflows](#cicd-and-governance-workflows)
- [Downstream Implementation](#downstream-implementation)
- [Validation](#validation)
- [Roadmap](#roadmap)
- [Cross-References](#cross-references)
- [Contributing](#contributing)
- [License](#license)
- [Author and Contact](#author-and-contact)

---

## Problem Statement

Creative knowledge management systems fail creative practitioners in three compounding ways.

First, they fragment. A writer's notes live in one application, their code experiments in another, their archived threads in a third. Each tool imposes its own organizational logic — folders here, tags there, relational databases elsewhere — and none of them talk to each other in terms the practitioner actually thinks in. The result is not a knowledge base but a knowledge scatter: dozens of disconnected containers with no shared grammar.

Second, they flatten. Most systems treat all knowledge as equivalent: a tag is a tag, a folder is a folder, a file is a file. But creative and theoretical work is *hierarchically recursive* — an idea contains sub-ideas that reference parent ideas that generate new ideas. Flat organizational schemes cannot represent this nesting without losing the structural relationships that make the knowledge meaningful.

Third, they stagnate. Traditional knowledge management treats storage as the terminal act: capture the note, file it, retrieve it later. But creative-theoretical work requires that knowledge *transform* — that raw material dissolves into patterns, patterns recompose into structures, structures return as new raw material for the next cycle. The system must not merely store; it must participate in the alchemical loop.

Radix Recursiva addresses all three failures with a single architecture. RE:GE:OS (Recursive Generative Operating System) is a symbolic operating system that encodes organizational meaning directly into its naming conventions, provides safe containment for experimental code through a zero-dependency Python sandbox, and integrates with Obsidian as a knowledge vault where the specification and its implementation are unified in a single recursive structure. The vault *is* the system. The directory layout *is* the logic. The names *are* the semantics.

---

## Core Concepts

### RE:GE:OS — Recursive Generative Operating System

RE:GE:OS is the theoretical spine of this repository. It is not a traditional operating system in the kernel/scheduler sense — it is an *organizational operating system* that governs how knowledge, experiments, and creative artifacts are structured, named, routed, and transformed within the vault.

The core principle is that **structure encodes meaning**. A file's location in the directory tree is not incidental — it declares the file's ontological status. A file in `REGEOS_RG01/` is a constitutional document. A file in `ARCHIVE_RK01/` is sealed history. A file in `SYSTEM_MAP_SM01/` is a living architectural experiment. Moving a file between directories is a *semantic operation*, not a housekeeping task.

RE:GE:OS operates through three interlocking mechanisms:

1. **Symbolic Law** — The UID Constitution (v2) governs all naming. Identifiers use consonant-only encoding (`AB-CD_12-34` expanded, `ABCD1234` condensed) to produce dense, semantically loaded names. The repository UID `4_S0VRC3` itself follows this convention — read phonetically as "A Source," it declares the vault's role as the origin point of the recursive system.

2. **Organizational Bodies** — 22 named archetypes (Heart of Canon, Mirror Cabinet, Code Forge, Echo Shell, Dream Council, Experimental Habitat, and others) map creative functions to mythic roles. Each body has a defined input ritual, function, mythic interpretation, and cross-reference map. They are not metaphors — they are *interface specifications* for different modes of creative-theoretical work.

3. **Recursive Self-Reference** — The system documents itself using its own conventions. The specification for how to name files is itself a file that follows the naming convention. The containment system for experiments is itself an experiment that graduated from containment. This is not a bug or a clever trick — it is the *solve-coagula-redi* loop made architectural.

### The Experimental Habitat System

The Python package at `src/habitat/` is the executable core of RE:GE:OS — a zero-dependency containment sandbox that manages the complete lifecycle of code experiments. It uses only the Python standard library (no pip packages required for core functionality), making it deployable in any Python 3.7+ environment without network access or package management.

The Habitat implements a biologically-inspired lifecycle:

```
Spawn → Run → { Graduate | Compost }
```

- **Spawn**: An experiment is created within a `ContainmentBoundary` — a hierarchical isolation structure that prevents experimental code from contaminating the broader system. Each boundary has a defined isolation level, resource limits, and a full containment path.
- **Run**: The experiment executes within its boundary. Execution time, resource usage, and results are tracked automatically. Failures are caught and contained rather than propagated.
- **Graduate**: Successful experiments are packaged with extracted code patterns, symbolic mappings, and integration hooks, then promoted to the Code Forge (organizational body #6) for integration into the production system.
- **Compost**: Failed experiments are not discarded — they are decomposed into *lessons*: what failed, what patterns emerged, what resources were consumed, and what reusable components can be salvaged. Even failure feeds the recursive loop.

The key architectural insight is **nested containment**: habitats can contain sub-habitats, each at a higher isolation level. This is the "hat on a hat on a hat" principle — Layer 1 provides the base environment, Layer 2 wraps it in an experimental container, Layer 3 adds test protocols, Layer 4 adds monitoring, and Layer 5+ allows recursive sub-experiments. Each layer inherits the constraints of its parent while adding its own.

Security is enforced at the containment level. Experiment names are validated against strict alphanumeric whitelists. Path traversal attacks are blocked through multiple defense-in-depth layers: regex validation, `..` sequence rejection, absolute path rejection, drive letter rejection, and `os.path.commonpath` verification. A path traversal vulnerability discovered in January 2026 prompted a comprehensive security hardening pass with 23 malicious pattern tests.

### Symbolic UID Naming Convention

Every identifier in this system follows a consonant-only UID convention governed by the UID Constitution (v2). The convention strips vowels from semantic keywords and encodes them as dense, portable identifiers:

| Format | Pattern | Example | Use |
|--------|---------|---------|-----|
| Expanded | `AB-CD_12-34` | `CM-CN_03-04` | Markdown comments, section headers |
| Condensed | `ABCD1234` | `CMCN0304` | File names, folder prefixes, asset registries |

Directory suffixes encode organizational function through 4-letter codes:

| Suffix | Meaning | Directory |
|--------|---------|-----------|
| `RG01` | RE:GE:OS Core | `REGEOS_RG01/` |
| `RK01` | Archive (Ark) | `ARCHIVE_RK01/` |
| `MR01` | Mirror | `MIRROR_MR01/` |
| `TP01` | Templates | `TEMPLATES_TP01/` |
| `TA01` | Tags | `TAGS_TA01/` |
| `SM01` | System Map | `SYSTEM_MAP_SM01/` |
| `FL01` | Anomalies (Flags) | `ANOMALIES_FL01/` |
| `FR01` | Fragments | `FRAGMENTS_FR01/` |
| `NR01` | Narratives | `NARRATIVES_NR01/` |
| `GD01` | Game Design | `GAMEDESIGN_GD01/` |
| `GT01` | Gateway | `GATEWAY_GT01/` |
| `WR01` | Workshops | `WORKSHOPS_WR01/` |

The naming system was frozen as of 2025-05-04 and serves as the constitutional basis for all vault operations. Every folder requires a `UID_MAP.md` (listing all UIDs), `REVISION_HISTORY.md` (documenting UID-level changes), and `README.md` (high-level overview with UID prefix explanation).

### The 22 Organizational Bodies

RE:GE:OS defines 22 named bodies, each representing a distinct creative-operational function within the system. Each body is specified with an input ritual, a declared function, a mythic interpretation (mapping the function to archetypal roles), and a referential cross-map (connecting it to analogous systems in computing, mythology, and organizational theory).

Selected bodies and their functions:

| # | Body | Function |
|---|------|----------|
| 00 | Academia Wing Protocol | Pedagogical cycle management and curriculum architecture |
| 01 | Heart of Canon | Core textual authority — the constitutional center of the system |
| 02 | Mirror Cabinet | Reflection, self-reference, and recursive self-observation |
| 03 | Mythic Senate | Deliberative judgment on narrative and symbolic decisions |
| 04 | Archive Order | Long-term preservation and archival governance |
| 05 | Ritual Court | Procedural frameworks and operational ceremony |
| 06 | Code Forge | Symbolic-to-executable transmutation — "Let this become structure" |
| 07 | Bloom Engine | Growth, emergence, and organic system development |
| 08 | Soul Patchbay | Routing and connection between disparate system components |
| 09 | Echo Shell | Resonance, feedback loops, and signal amplification |
| 10 | Dream Council | Speculative and generative ideation |
| 11 | Mask Engine | Identity management and contextual persona switching |
| 12 | Chamber of Commerce | Economic logic and value exchange within the system |
| 13 | Blockchain Economy | Immutable record-keeping and trust-less verification |
| 14 | Process Monetizer | Converting process artifacts into distributable value |
| 15 | Audience Engine | Attention management and reception dynamics |
| 16 | Place Protocols | Spatial and contextual awareness logic |
| 17 | Time Rules Engine | Temporal governance — deadlines, rhythms, scheduling |
| 18 | Analog-Digital Engine | Translation between physical and digital modalities |
| 19 | Process-Product Converter | Transmuting creative process into deliverable product |
| 20 | Consumption Protocol | How artifacts are received, consumed, and metabolized |
| 21 | Stagecraft Module | Performance, presentation, and theatrical logic |
| 22 | Publishing Temple | Final-form output and public distribution |
| 23 | Experimental Habitat | Containment, safe experimentation, recursive nesting |

These are not decorative labels. Each body defines an *interface contract* — a specified way of interacting with a particular mode of creative-theoretical work. When an experiment graduates from the Habitat (body 23) to the Code Forge (body 6), that transition follows a defined protocol with extracted patterns, symbolic mappings, and integration hooks.

### Obsidian Knowledge Vault Integration

The repository is simultaneously a Git repository and an Obsidian vault. The `.obsidian/` directory contains full plugin configuration for 20+ plugins including Dataview, Excalidraw, Kanban, Smart Connections, Text Generator, Copilot, Templater, and Omnisearch. The vault is synced via Obsidian Sync (iCloud support was deprecated in the v2025-05-04 refresh).

This dual nature is intentional. Obsidian provides the *experiential* interface — graph views that visualize knowledge connections, daily notes that track operational rhythms, templates that enforce UID conventions, and backlinks that make the recursive structure navigable. Git provides the *archival* interface — version history, branch-based experimentation, collaborative review, and CI/CD automation. The vault is the living workspace; Git is the institutional memory.

The `.makemd/` and `.space/` directories provide additional metadata layers for enhanced navigation and contextual workspace organization within the Obsidian environment.

---

## Architecture

### Directory Ontology

The directory structure is not a filing system — it is an ontological map. Each top-level directory occupies a defined position in the knowledge lifecycle:

```
radix-recursiva-solve-coagula-redi/
├── REGEOS_RG01/                    # Constitutional core — symbolic laws, 22 bodies
├── DOCUMENTATION/                  # SOPs, guides, policies, cookbooks, standards
│   ├── sops/                       # Daily/weekly/monthly operational checklists
│   ├── guides/                     # Vault guide, glossary, habitat docs
│   └── courses/                    # Pedagogical materials (D2L exports)
├── TEMPLATES_TP01/                 # Seed files, note templates
├── TAGS_TA01/                      # Tag and symbol management
├── CATALOGS_AND_INDEXES/           # Master indexes, UID registries, observation logs
│   └── uids/                       # UID Constitution, master index, audit logs
├── src/habitat/                    # Python package — Experimental Habitat System
├── scripts/                        # CLI tools, vault utilities, validation
│   ├── vault_utils/                # UID generation, indexing, checking, routing
│   ├── analysis/                   # Analytical tools
│   └── jules/                      # AI agent integration scripts
├── tests/                          # Pytest test suite
├── ARCHIVE_RK01/                   # Sealed archival storage (legacy exports)
├── MIRROR_MR01/                    # Shadow self, reflection systems
├── SYSTEM_MAP_SM01/                # System architecture experiments
├── ARCHIVAL_STACK/                 # Project thread digests (per-project logs)
├── PROJECT_MANAGEMENT/             # Changelogs, manifests, meta-operations
├── ANOMALIES_FL01/                 # Anomaly tracking
├── FRAGMENTS_FR01/                 # Fragment and memory collection
├── NARRATIVES_NR01/                # Narrative content
├── GAMEDESIGN_GD01/                # Game design materials
├── WORKSHOPS_WR01/                 # Workshop content
├── GATEWAY_GT01/                   # External ingestion points
├── security/                       # Recovery keys (isolated)
└── .github/workflows/              # 17 CI/CD workflows
```

### Python Package Structure

The `src/habitat/` package exports five primary components:

```python
from habitat import (
    ExperimentalHabitat,    # Main containment environment
    ExperimentalSystem,     # Base class for all experiments
    ContainmentBoundary,    # Hierarchical isolation structure
    RecursiveMythEngine,    # Built-in example: recursive myth generation
    HabitatManager,         # CLI management interface
)
```

**`ExperimentalHabitat`** is the primary entry point. It manages a temporary workspace directory, tracks active/graduated/failed experiments, maintains containment boundaries, and provides methods for spawning, running, nesting, graduating, and composting experiments.

**`ContainmentBoundary`** implements hierarchical isolation. Each boundary has a name, isolation level, optional parent, and child list. The `get_full_path()` method returns the complete containment path (e.g., `boundary_myth_engine/nested_analyzer/sub_test`), making the nesting structure explicit and traceable.

**`RecursiveMythEngine`** is both a demonstration and a declaration: it generates recursive mythic patterns that nest to a configurable depth, producing self-referential structures like *"In the beginning was the word, and the word contained: At depth 3, the mirror reflects itself infinitely."* It is the system's own logic rendered as output.

**`HabitatManager`** provides the CLI interface with full CRUD operations for experiments, JSON configuration persistence, and colored terminal output via the `habitat_ux` module.

### Data Flow: Solve, Coagula, Redi in Practice

The alchemical cycle maps directly to system operations:

1. **Solve** (Dissolution) — Raw material enters through `GATEWAY_GT01/` or is spawned as an `ExperimentalSystem`. It is dissolved into components: hypothesis, containment rules, resource requirements, symbolic classification.

2. **Coagula** (Recomposition) — The experiment runs within its `ContainmentBoundary`. Results are extracted, patterns are identified, symbolic mappings are generated. Successful experiments are packaged into forge-ready bundles; failed experiments are decomposed into lessons.

3. **Redi** (Return) — Graduated patterns integrate back into the system through the Code Forge. Composted lessons feed into the Mirror Cabinet for reflection. The system returns to its starting state, enriched by the cycle. The next experiment begins.

---

## Installation and Usage

### Prerequisites

- Python 3.7 or later (standard library only — zero external dependencies for core functionality)

### Setup

```bash
# Clone the repository
git clone https://github.com/organvm-i-theoria/radix-recursiva-solve-coagula-redi.git
cd radix-recursiva-solve-coagula-redi

# Install the habitat package (editable mode)
pip install -e .

# Optional: install development dependencies (pytest, black, flake8)
pip install -e ".[dev]"
```

### CLI Entry Points

After installation, four console commands are available:

| Command | Purpose |
|---------|---------|
| `habitat-manager` | Full habitat containment system management |
| `habitat-interactive` | Interactive habitat interface for exploration |
| `habitat-demo` | Quick demonstration of core concepts |
| `habitat-workflow` | Complete end-to-end workflow demonstration |

### Programmatic Usage

```python
from habitat import ExperimentalHabitat, ExperimentalSystem

# Create a habitat with isolation level 3
lab = ExperimentalHabitat("my_lab", isolation_level=3)

# Define and spawn an experiment
experiment = ExperimentalSystem("test_hypothesis", "Recursive patterns stabilize at depth 4")
lab.spawn_experiment(experiment, {
    'resources': {'cpu': '50%', 'memory': '512M'},
    'network_isolation': True,
    'recursive_depth_limit': 5
})

# Run the experiment
result = lab.run_experiment("test_hypothesis")

# Graduate or compost based on results
if result.get('success'):
    forge_package = lab.graduate_to_forge("test_hypothesis")
else:
    lessons = lab.contain_failure("test_hypothesis", "Hypothesis disproven")

# Always clean up
lab.cleanup()
```

---

## Examples

### Running the Recursive Myth Engine

```bash
$ habitat-demo
 'A HAT ON A HAT ON A' - EXPERIMENTAL CONTAINMENT DEMO
============================================================
Creating layered experimental environments...

 Layer 1: Creating base experimental habitat...
   [OK] Base habitat established: base_creative_lab
   [OK] Experiment spawned: recursive_myth_engine
   [LOCKED] Containment boundary: boundary_recursive_myth_engine

 Layer 2: Creating nested habitat within experiment...
   [OK] Nested habitat created: base_creative_lab_nested_recursive_analysis_lab
   [INFO] Nesting depth: 1
   [LOCKED] Isolation level: 2
```

### Creating Nested Containment

```python
from habitat import ExperimentalHabitat, ExperimentalSystem

# Base habitat
base = ExperimentalHabitat("outer_lab", isolation_level=1)

# Spawn parent experiment
parent = ExperimentalSystem("parent_test", "Testing nesting behavior")
base.spawn_experiment(parent, {'resources': {'cpu': '75%'}})

# Create nested habitat inside the parent experiment
nested = base.nest_habitat("parent_test", "inner_lab")
# nested.isolation_level == 2 (automatically incremented)
# nested.nesting_depth == 1

# Spawn child experiment in nested habitat
child = ExperimentalSystem("child_test", "Testing deeper containment")
nested.spawn_experiment(child, {'resources': {'cpu': '50%'}})
```

### Managing Experiments via CLI

```bash
# Spawn a new experiment
habitat-manager spawn my_experiment --hypothesis "Testing symbolic resonance patterns"

# Check status
habitat-manager status my_experiment

# Run the experiment
habitat-manager run my_experiment

# Graduate successful experiments to the Code Forge
habitat-manager graduate my_experiment

# Or compost failed experiments for lessons
habitat-manager compost my_experiment --reason "Recursive depth exceeded safe limits"

# Clean up all habitats
habitat-manager cleanup
```

---

## Vault Utilities and Automation

The `scripts/` directory provides automation tools for vault operations:

| Script | Purpose |
|--------|---------|
| `vault_utils/generate_uid.py` | Generate new consonant-only symbolic UIDs |
| `vault_utils/uid_indexer.py` | Regenerate the master UID index |
| `vault_utils/uid_check.py` | Validate UID compliance across the vault |
| `vault_utils/initialize_vault.py` | Bootstrap the full folder structure from scratch |
| `vault_utils/vault_freeze.py` | Create archival snapshots for long-term preservation |
| `vault_utils/sort_router.py` | Route incoming files to their correct domain folders |
| `validate_containment.py` | Check containment policy compliance |
| `metadata_guard.py` | Validate YAML frontmatter across all markdown files |
| `check_env_vars.py` | Verify required environment variables are set |

---

## CI/CD and Governance Workflows

The repository includes 17 GitHub Actions workflows in `.github/workflows/`:

- **Security**: CodeQL analysis, Semgrep static analysis, Pyre type checking
- **Quality**: ESLint, Hadolint (Dockerfile linting), documentation quality checks, reviewdog markdown review
- **AI Integration**: AI-assisted PR review, commit agent, knowledge governance
- **Branch Management**: Jules branch guard (managing `bolt-*/sentinel-*/palette-*` branch prefixes), Jules cleanup, Jules preflight
- **Deployment**: Jekyll GitHub Pages, summary generation, label automation

---

## Downstream Implementation

As an ORGAN-I (Theory) repository, Radix Recursiva provides foundational patterns that flow downstream to ORGAN-II (Poiesis/Art) and ORGAN-III (Ergon/Commerce):

- **ORGAN-II**: The Experimental Habitat lifecycle (Spawn/Run/Graduate/Compost) provides the containment architecture for generative art experiments in [`organvm-ii-poiesis`](https://github.com/organvm-ii-poiesis). The 22 organizational bodies — particularly the Stagecraft Module (#21), the Bloom Engine (#7), and the Mask Engine (#11) — define the symbolic grammar that ORGAN-II creative projects implement as experiential artifacts.

- **ORGAN-III**: The Process-Product Converter (body #19), the Chamber of Commerce (body #12), and the Process Monetizer (body #14) encode the theoretical framework for how creative process becomes commercial product in [`organvm-iii-ergon`](https://github.com/organvm-iii-ergon). The UID naming convention provides the cross-organ referencing system that connects theoretical specifications to their commercial implementations.

- **ORGAN-IV**: The governance patterns in the SOP framework (daily/weekly/monthly checklists) and the promotion lifecycle (Spawn/Graduate/Compost) inform the orchestration logic in [`organvm-iv-taxis`](https://github.com/organvm-iv-taxis), particularly the [`agentic-titan`](https://github.com/organvm-iv-taxis/agentic-titan) coordination system.

The dependency flow is strictly unidirectional: I to II to III. ORGAN-III cannot depend on ORGAN-II internals, and ORGAN-II cannot modify ORGAN-I specifications. This is enforced by the eight-organ system's no-back-edges invariant.

---

## Validation

| Criterion | Status |
|-----------|--------|
| Zero external dependencies (core) | Verified — `install_requires=[]` in `setup.py` |
| Python 3.7+ compatibility | Verified — type hints use `typing` module, no walrus operators |
| Path traversal prevention | Verified — 23 malicious patterns blocked (January 2026 security fix) |
| UID Constitution compliance | Verified — naming frozen 2025-05-04, all directories follow suffix convention |
| Containment boundary isolation | Verified — `os.path.commonpath` enforcement prevents directory escapes |
| Recursive nesting | Verified — `nest_habitat()` increments isolation level per depth |
| Experiment lifecycle completeness | Verified — Spawn, Run, Graduate, Compost all implemented with logging |
| Test suite | Present — pytest integration covering habitat UX, metadata guard, environment checks, AI reviewer, commit agent |

---

## Roadmap

- [ ] **Containment Metrics Dashboard** — Real-time visualization of active experiments, resource usage, and containment boundary health
- [ ] **Distributed Habitat Federation** — Networking multiple habitat instances across repositories for cross-organ experimentation
- [ ] **Pattern Library** — Searchable catalog of graduated patterns extracted from successful experiments
- [ ] **Symbolic UID v3** — Extended UID encoding supporting hierarchical namespace nesting and cross-vault references
- [ ] **SOP Automation** — Scripted execution of daily/weekly/monthly operational checklists with automated validation
- [ ] **Obsidian Plugin** — Custom Obsidian plugin for direct habitat management from within the vault interface

---

## Cross-References

| Document | Location | Purpose |
|----------|----------|---------|
| CLAUDE.md | [`CLAUDE.md`](CLAUDE.md) | Full command reference and development setup |
| UID Constitution v2 | `CATALOGS_AND_INDEXES/uids/UID_Constitution_v2.md` | Governing document for all naming conventions |
| System Root README | `REGEOS_RG01/SYSTEM_ROOT_README.md` | Central navigation index for the vault |
| SEAL v2a Final | `REGEOS_RG01/SEAL_v2a_FINAL.md` | System declaration and structural confirmation |
| SOP System Overview | `DOCUMENTATION/sops/SOP_SYSTEM_OVERVIEW.md` | Complete operations manual |
| Glossary | `DOCUMENTATION/guides/GLOSSARY.md` | Symbolic terminology reference |
| Master UID Index | `CATALOGS_AND_INDEXES/uids/UIDS_MASTER_INDEX.md` | Complete UID registry |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) | Structural changes and security fixes |

---

## Contributing

Contributions are welcome. This repository operates on an AI-conductor model: AI generates volume, human reviews and refines. When contributing:

1. Read the [Community Guidelines](.github/COMMUNITY_GUIDELINES.md) and the UID Constitution (`CATALOGS_AND_INDEXES/uids/UID_Constitution_v2.md`)
2. All new files must follow the UID naming convention — consonant-only identifiers with appropriate suffix codes
3. Experimental code must be contained within the Habitat system — do not add dependencies outside the Python standard library
4. Use the [Discussion boards](https://github.com/organvm-i-theoria/radix-recursiva-solve-coagula-redi/discussions) for questions and ideas
5. Submit issues using the provided templates (bug report, feature request, promotion request)

---

## License

This project is licensed under the MIT License.

---

## Author and Contact

**Anthony James Padavano** — [@4444J99](https://github.com/4444J99)

System Architect / Writer / Instructor / Artist / Gamewright
`4_S0VRC3 // v2a FINAL`

---

## Part of the Eight-Organ System

This repository belongs to **ORGAN-I: Theoria** — the epistemological and theoretical foundation of the [organvm](https://github.com/meta-organvm) creative-institutional system.

| Organ | Domain | Organization |
|-------|--------|-------------|
| **I — Theoria** | Theory, epistemology, recursion | [`organvm-i-theoria`](https://github.com/organvm-i-theoria) |
| II — Poiesis | Art, generative and experiential | [`organvm-ii-poiesis`](https://github.com/organvm-ii-poiesis) |
| III — Ergon | Commerce, SaaS and products | [`organvm-iii-ergon`](https://github.com/organvm-iii-ergon) |
| IV — Taxis | Orchestration and governance | [`organvm-iv-taxis`](https://github.com/organvm-iv-taxis) |
| V — Logos | Public process and essays | [`organvm-v-logos`](https://github.com/organvm-v-logos) |
| VI — Koinonia | Community and salons | [`organvm-vi-koinonia`](https://github.com/organvm-vi-koinonia) |
| VII — Kerygma | Marketing and distribution | [`organvm-vii-kerygma`](https://github.com/organvm-vii-kerygma) |
| VIII — Meta | Umbrella organization | [`meta-organvm`](https://github.com/meta-organvm) |

---

**[@4444J99](https://github.com/4444J99)** / Part of [ORGAN-I: Theoria](https://github.com/organvm-i-theoria)

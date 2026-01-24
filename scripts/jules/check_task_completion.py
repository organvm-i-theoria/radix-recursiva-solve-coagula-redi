#!/usr/bin/env python3
"""Check whether a Jules task is already complete.

Exit codes:
  0 -> task NOT detected (Jules may proceed)
  1 -> task already complete (Jules should skip)

This script is intentionally conservative: it only reports "complete" when all
required patterns for a signature are found.

It can inspect either:
- a git ref (default: origin/main) via `git show <ref>:<path>`; or
- the working tree, as a fallback.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class TaskSignature:
    files: tuple[str, ...]
    patterns: tuple[str, ...]
    description: str


TASK_SIGNATURES: dict[str, TaskSignature] = {
    # bolt: path caching optimization
    "bolt-optimize-containment": TaskSignature(
        files=("experimental_habitat_implementation.py",),
        patterns=(r"self\._full_path\s*=", r"_update_full_path|get_full_path\(\)"),
        description="Path caching optimization",
    ),
    # sentinel: path traversal validation
    "sentinel-path-traversal": TaskSignature(
        files=("experimental_habitat_implementation.py",),
        patterns=(
            r"def _validate_experiment_name",
            r"\.{2}|\.\./|path traversal|not allowed",
        ),
        description="Path traversal validation",
    ),
    # palette: CLI card UX pattern
    "palette-cli-cards": TaskSignature(
        files=("habitat_ux.py", "habitat_manager.py"),
        patterns=(r"def print_card", r"habitat_ux\.print_card"),
        description="CLI card pattern",
    ),
}


def _run_git_show(repo_path: Path, ref: str, file_path: str) -> Optional[str]:
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{file_path}"],
            cwd=str(repo_path),
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None


def _read_working_tree(repo_path: Path, file_path: str) -> Optional[str]:
    p = repo_path / file_path
    if not p.exists() or not p.is_file():
        return None
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Best-effort fallback
        return p.read_text(errors="replace")


def _fuzzy_match_signature(task_type: str) -> Optional[TaskSignature]:
    normalized = (task_type or "").strip().lower()
    if not normalized:
        return None

    # Prefer exact key match.
    if normalized in TASK_SIGNATURES:
        return TASK_SIGNATURES[normalized]

    # Otherwise accept substring containment (covers e.g. "bolt-optimize-containment-path-123").
    for key, sig in TASK_SIGNATURES.items():
        if key in normalized:
            return sig

    return None


def _all_patterns_present(patterns: Iterable[str], content: str) -> bool:
    return all(
        re.search(p, content, flags=re.IGNORECASE | re.MULTILINE) for p in patterns
    )


def check_task_complete(task_type: str, repo_path: Path, ref: str) -> bool:
    sig = _fuzzy_match_signature(task_type)
    if not sig:
        print(f"ℹ️  Unknown task type: {task_type}")
        return False

    print(f"🔍 Checking for: {sig.description}")
    print(f"   Task type: {task_type}")
    print(f"   Repo path: {repo_path}")
    print(f"   Ref:       {ref}")

    for file_path in sig.files:
        content = _run_git_show(repo_path, ref, file_path)
        source = f"{ref}:{file_path}"
        if content is None:
            content = _read_working_tree(repo_path, file_path)
            source = str(repo_path / file_path)

        if content is None:
            continue

        if _all_patterns_present(sig.patterns, content):
            print(f"✅ Task '{sig.description}' already complete")
            print(f"   Found in: {source}")
            return True

    print("❌ Task not complete")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check if a Jules task is already complete"
    )
    parser.add_argument(
        "--task-type",
        required=True,
        help="Task type (e.g., bolt-optimize-containment, sentinel-path-traversal, palette-cli-cards)",
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Path to repository (default: current directory)",
    )
    parser.add_argument(
        "--ref",
        default="origin/main",
        help="Git ref to inspect (default: origin/main)",
    )

    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()

    complete = check_task_complete(args.task_type, repo_path, args.ref)
    if complete:
        print("\n🛑 STOP: Task already complete — skipping branch creation")
        return 1

    print("\n✅ PROCEED: Task not complete — Jules may run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

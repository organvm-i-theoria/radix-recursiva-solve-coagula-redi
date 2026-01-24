#!/usr/bin/env python3
"""Check whether a base ref is "fresh" enough.

This is intended as a guardrail against bots branching from very old commits.

Exit codes:
  0 -> base ref is fresh (<= max-age-days)
  1 -> base ref is stale (> max-age-days)
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class FreshnessResult:
    base_ref: str
    commit_sha: str
    age_days: int


def _git(repo_path: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=str(repo_path), text=True
    ).strip()


def get_commit_age_days(repo_path: Path, ref: str) -> FreshnessResult:
    sha = _git(repo_path, "rev-parse", ref)
    ts = int(_git(repo_path, "show", "-s", "--format=%ct", sha))
    commit_dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)
    age_days = (now - commit_dt).days
    return FreshnessResult(base_ref=ref, commit_sha=sha, age_days=age_days)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check base ref freshness")
    parser.add_argument("--repo-path", default=".", help="Path to repo (default: .)")
    parser.add_argument(
        "--base-ref",
        default="origin/main",
        help="Base ref to check (default: origin/main)",
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=7,
        help="Max acceptable age in days (default: 7)",
    )

    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()

    # Ensure refs are available.
    subprocess.run(
        ["git", "fetch", "--prune", "origin"], cwd=str(repo_path), check=False
    )

    res = get_commit_age_days(repo_path, args.base_ref)
    print(f"🔎 Base ref:   {res.base_ref}")
    print(f"🔎 Commit SHA: {res.commit_sha}")
    print(f"🕒 Age (days): {res.age_days}")

    if res.age_days > args.max_age_days:
        print(
            f"❌ Base ref is stale: {res.age_days}d old (max allowed: {args.max_age_days}d)"
        )
        print("🛑 STOP: Refuse to branch from a stale base")
        return 1

    print(f"✅ Base ref is fresh enough (≤ {args.max_age_days} days)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

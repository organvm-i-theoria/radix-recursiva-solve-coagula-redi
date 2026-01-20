#!/usr/bin/env python3
"""Cleanup stale Jules branches by prefix and age.

This script can be used locally or from CI. It uses `git` to list remote refs
and optionally deletes them via `git push <remote> --delete <branch>`.

Safety:
- Only deletes branches whose names start with configured prefixes.
- Never deletes the repository default branches (main/master) even if prefixes match.

Exit code:
  0 -> completed (even if nothing deleted)
  2 -> nothing deleted because in dry-run mode (still success)
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Tuple


DEFAULT_PREFIXES = ["bolt-", "sentinel-", "palette-"]


@dataclass(frozen=True)
class RemoteBranch:
    name: str
    committer_unix: int

    @property
    def age_days(self) -> int:
        now = int(datetime.now(tz=timezone.utc).timestamp())
        return (now - self.committer_unix) // 86400


def _run(
    repo_path: Path, args: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=str(repo_path), text=True, capture_output=True, check=check
    )


def list_remote_branches(repo_path: Path, remote: str) -> List[RemoteBranch]:
    # Ensure remote refs are up-to-date.
    _run(repo_path, ["git", "fetch", "--prune", remote], check=False)

    cp = _run(
        repo_path,
        [
            "git",
            "for-each-ref",
            f"refs/remotes/{remote}",
            "--format=%(refname:short) %(committerdate:unix)",
        ],
    )

    branches: List[RemoteBranch] = []
    for line in cp.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ref, ts = line.split(" ", 1)
            branches.append(RemoteBranch(name=ref, committer_unix=int(ts)))
        except ValueError:
            continue

    return branches


def filter_stale(
    branches: Iterable[RemoteBranch],
    *,
    remote: str,
    prefixes: Tuple[str, ...],
    max_age_days: int,
) -> List[RemoteBranch]:
    stale: List[RemoteBranch] = []
    protected = {f"{remote}/main", f"{remote}/master"}

    for b in branches:
        if b.name in protected:
            continue

        if not b.name.startswith(f"{remote}/"):
            continue

        short = b.name[len(f"{remote}/") :]
        if not any(short.startswith(p) for p in prefixes):
            continue

        if b.age_days > max_age_days:
            stale.append(b)

    stale.sort(key=lambda x: x.committer_unix)
    return stale


def delete_remote_branch(repo_path: Path, remote: str, branch_short: str) -> None:
    _run(repo_path, ["git", "push", remote, "--delete", branch_short], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Delete stale Jules branches by prefix"
    )
    parser.add_argument("--repo-path", default=".", help="Path to repository")
    parser.add_argument(
        "--remote", default="origin", help="Remote name (default: origin)"
    )
    parser.add_argument(
        "--prefix",
        action="append",
        default=None,
        help="Branch prefix to match (repeatable). Defaults to bolt-/sentinel-/palette-.",
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=30,
        help="Delete branches older than this (default: 30)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted, but do not delete",
    )

    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    prefixes = tuple(args.prefix or DEFAULT_PREFIXES)

    branches = list_remote_branches(repo_path, args.remote)
    stale = filter_stale(
        branches, remote=args.remote, prefixes=prefixes, max_age_days=args.max_age_days
    )

    print(f"🔍 Remote: {args.remote}")
    print(f"🔍 Prefixes: {', '.join(prefixes)}")
    print(f"🕒 Max age: {args.max_age_days} days")
    print(f"📌 Found {len(stale)} stale branches")

    if not stale:
        return 0

    for b in stale:
        short = b.name[len(f"{args.remote}/") :]
        print(f"  - {short} ({b.age_days} days old)")

    if args.dry_run:
        print("\n🧪 Dry run enabled: no branches deleted")
        return 2

    deleted = 0
    for b in stale:
        short = b.name[len(f"{args.remote}/") :]
        print(f"🗑️  Deleting {short}...")
        delete_remote_branch(repo_path, args.remote, short)
        deleted += 1

    print(f"\n✅ Deleted {deleted} branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

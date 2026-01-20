"""Jules coordination utilities.

These helper scripts are designed to reduce branch proliferation by:
- detecting when a task is already complete on the default branch
- enforcing basic base-branch freshness checks
- cleaning up stale bot-created branches

They are safe to run locally and can also be used from GitHub Actions.
"""

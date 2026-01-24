"""
UID CHECK SCRIPT
Scans all markdown files in a given directory for duplicate or malformed UIDs.
"""

import os
import re
from collections import defaultdict

def scan_uids(base_path):
    uid_pattern = re.compile(r"[A-Z]{2}-[A-Z]{2}_[0-9]{2}-[0-9]{2}")
    seen = defaultdict(list)

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), 'r') as f:
                    for i, line in enumerate(f):
                        matches = uid_pattern.findall(line)
                        for uid in matches:
                            seen[uid].append((file, i + 1))

    print("UID Report:")
    for uid, locations in seen.items():
        print(f"{uid} found in {len(locations)} locations:")
        for file, line in locations:
            print(f"  - {file} (line {line})")

if __name__ == "__main__":
    scan_uids(".")

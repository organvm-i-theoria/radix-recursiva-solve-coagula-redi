"""
TIMELINE MAP SCRIPT
Generates a week-by-week plan from a calendar map file and outputs a summary.
"""

import os
import sys

def load_calendar_file(calendar_file):
    with open(calendar_file, 'r') as f:
        lines = f.readlines()

    weeks = []
    current_week = None
    for line in lines:
        if line.strip().startswith("## Week"):
            current_week = {'header': line.strip(), 'lines': []}
            weeks.append(current_week)
        elif current_week:
            current_week['lines'].append(line.strip())
    return weeks

def display_timeline(calendar_file):
    print(f"--- Timeline Overview from: {calendar_file} ---")
    weeks = load_calendar_file(calendar_file)
    for week in weeks:
        print(week['header'])
        for line in week['lines']:
            if line:
                print("  " + line)
        print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python timeline_map.py [calendar_file.md]")
    else:
        display_timeline(sys.argv[1])

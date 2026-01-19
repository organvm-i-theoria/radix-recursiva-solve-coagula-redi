"""
HABITAT_UX.py

UX utilities for the Experimental Habitat system.
Implements the 'CLI Card Pattern' for consistent, readable output.
"""

import shutil
import textwrap
import pprint

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_terminal_width():
    return shutil.get_terminal_size((80, 20)).columns

def print_card(title: str, data: dict, icon: str = "ℹ️", color: str = None):
    """Prints a formatted card with a title and key-value pairs."""
    width = min(get_terminal_width(), 80)
    content_width = width - 4

    # Header
    print(f"\n╭─ {icon} {title} {'─' * (width - len(title) - 6)}╮")

    # Body
    for key, value in data.items():
        key_str = f"│ {key}: "
        indent = "│   "

        # Format complex values
        if isinstance(value, (dict, list)):
            val_str = pprint.pformat(value, width=content_width - len(indent))
        else:
            val_str = str(value)

        # Wrap long text
        wrapped_lines = textwrap.wrap(
            val_str,
            width=content_width - len(key_str) + len(indent),
            subsequent_indent=indent
        )

        if not wrapped_lines:
            print(f"{key_str}")
            continue

        print(f"{key_str}{wrapped_lines[0]}")
        for line in wrapped_lines[1:]:
             print(f"{indent}{line}")

    # Footer
    print(f"╰{'─' * (width - 2)}╯")

def print_header(title: str, subtitle: str = None):
    """Prints a main header."""
    width = min(get_terminal_width(), 80)
    print(f"\n{'=' * width}")
    print(f" {title.center(width - 2)}")
    if subtitle:
        print(f" {subtitle.center(width - 2)}")
    print(f"{'=' * width}\n")

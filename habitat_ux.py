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

    c_start = color if color else ""
    c_end = Colors.RESET if color else ""

    # Header
    print(f"\n{c_start}╭─ {icon} {title} {'─' * (width - len(title) - 6)}╮{c_end}")

    # Body
    for key, value in data.items():
        # Visual strings for length calculation
        plain_key_str = f"│ {key}: "
        plain_indent = "│   "

        # Colored strings for printing
        colored_key_str = f"{c_start}│{c_end} {key}: "
        colored_indent = f"{c_start}│{c_end}   "

        # Format complex values
        if isinstance(value, (dict, list)):
            val_str = pprint.pformat(value, width=content_width - len(plain_indent))
        else:
            val_str = str(value)

        # Wrap long text
        wrapped_lines = textwrap.wrap(
            val_str,
            width=content_width - len(plain_key_str) + len(plain_indent)
        )

        if not wrapped_lines:
            print(f"{colored_key_str}")
            continue

        print(f"{colored_key_str}{wrapped_lines[0]}")
        for line in wrapped_lines[1:]:
             print(f"{colored_indent}{line}")

    # Footer
    print(f"{c_start}╰{'─' * (width - 2)}╯{c_end}")

def print_header(title: str, subtitle: str = None, color: str = None):
    """Prints a main header."""
    width = min(get_terminal_width(), 80)
    c_start = color if color else ""
    c_end = Colors.RESET if color else ""

    print(f"\n{c_start}{'=' * width}{c_end}")
    print(f" {c_start}{title.center(width - 2)}{c_end}")
    if subtitle:
        print(f" {subtitle.center(width - 2)}")
    print(f"{c_start}{'=' * width}{c_end}\n")

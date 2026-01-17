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
    """Prints a formatted card with a title and key-value pairs.

    Args:
        title: The title of the card
        data: Dictionary of key-value pairs to display
        icon: Emoji icon for the header
        color: ANSI color code from Colors class to apply to borders and title
    """
    width = min(get_terminal_width(), 80)
    content_width = width - 4

    # Set color (default to empty string if None)
    c = color if color else ""
    r = Colors.RESET if color else ""

    # Header
    print(f"\n{c}╭─ {icon} {title} {'─' * (width - len(title) - 6)}╮{r}")

    # Body
    for key, value in data.items():
        key_str = f"{c}│{r} {key}: "
        indent = f"{c}│{r}   "

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
    print(f"{c}╰{'─' * (width - 2)}╯{r}")

def print_header(title: str, subtitle: str = None, color: str = None):
    """Prints a main header."""
    width = min(get_terminal_width(), 80)

    # Set color (default to empty string if None)
    c = color if color else ""
    r = Colors.RESET if color else ""

    print(f"\n{c}{'=' * width}{r}")
    print(f" {c}{title.center(width - 2)}{r}")
    if subtitle:
        print(f" {c}{subtitle.center(width - 2)}{r}")
    print(f"{c}{'=' * width}{r}\n")

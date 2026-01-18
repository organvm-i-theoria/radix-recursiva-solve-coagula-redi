"""
HABITAT_UX.py

UX utilities for the Experimental Habitat system.
Implements the 'CLI Card Pattern' for consistent, readable output.
"""

import shutil
import textwrap
import pprint

class Colors:
    """ANSI color codes for CLI output."""
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
    """
    Prints a formatted card with a title and key-value pairs.

    Args:
        title: The card title.
        data: Dictionary of data to display.
        icon: Icon to display before title.
        color: ANSI color code for borders and title (e.g., Colors.BLUE).
    """
    width = min(get_terminal_width(), 80)
    content_width = width - 4

    # Prepare color strings
    c = color if color else ""
    r = Colors.RESET if color else ""

    # Header
    # Note: We apply color to the border chars and title, but not the icon if we want to preserve its natural color?
    # Usually icons are emojis. Coloring them might change them in some terminals, or do nothing.
    # We'll wrap the whole header structure in color for simplicity, assuming title text is what we want colored.
    padding_len = max(0, width - len(title) - 6)
    print(f"\n{c}╭─ {icon} {title} {'─' * padding_len}╮{r}")

    # Body
    for key, value in data.items():
        # Plain strings for length calculations
        plain_key_str = f"│ {key}: "
        plain_indent_str = "│   "

        # Colored strings for output
        # We color the border '│' but keep the key text neutral (or we could bold it?)
        # The prompt says: "apply ANSI colors to the card's header, title, and side borders, while keeping content text neutral."
        # So we color '│'.
        colored_border = f"{c}│{r}"
        colored_key_str = f"{colored_border} {key}: "

        # Format complex values
        # indent for pprint must be spaces, we will prepend border later
        pprint_indent_len = len(plain_indent_str)
        if isinstance(value, (dict, list)):
            val_str = pprint.pformat(value, width=content_width - pprint_indent_len)
        else:
            val_str = str(value)

        # Wrap long text
        # subsequent_indent should be spaces. We will prepend the colored border manually.
        wrap_indent = "   " # 3 spaces, plus the border (1 char) makes 4 chars alignment

        wrapped_lines = textwrap.wrap(
            val_str,
            width=content_width - len(plain_key_str) + len(plain_indent_str),
            subsequent_indent=wrap_indent
        )

        if not wrapped_lines:
            print(f"{colored_key_str}")
            continue

        print(f"{colored_key_str}{wrapped_lines[0]}")
        for line in wrapped_lines[1:]:
             # line already starts with '   ' (wrap_indent)
             print(f"{colored_border}{line}")

    # Footer
    print(f"{c}╰{'─' * (width - 2)}╯{r}")

def print_header(title: str, subtitle: str = None, color: str = None):
    """Prints a main header."""
    width = min(get_terminal_width(), 80)
    c = color if color else ""
    r = Colors.RESET if color else ""

    print(f"\n{c}{'=' * width}{r}")
    print(f" {c}{title.center(width - 2)}{r}")
    if subtitle:
        print(f" {subtitle.center(width - 2)}")
    print(f"{c}{'=' * width}{r}\n")

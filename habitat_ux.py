"""
HABITAT_UX.py

UX utilities for the Experimental Habitat system.
Implements the 'CLI Card Pattern' for consistent, readable output.
"""

import shutil
import textwrap
import pprint
import re
import sys
import time
import threading
import itertools
from typing import Any


_ANSI_CSI_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
_ANSI_OSC_RE = re.compile(r"\x1B\].*?(?:\x07|\x1B\\)", re.DOTALL)
_ANSI_ESC_RE = re.compile(r"\x1B[@-Z\\-_]")


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from a string.

    Intended for sanitizing untrusted/user-controlled strings before printing.
    """
    if not text:
        return text
    text = _ANSI_OSC_RE.sub("", text)
    text = _ANSI_CSI_RE.sub("", text)
    text = _ANSI_ESC_RE.sub("", text)
    return text


def sanitize_for_terminal(value: Any, *, keep_newlines: bool = False) -> str:
    """Sanitize a value for safe-ish terminal display.

    - Strips ANSI escape sequences.
    - Replaces newlines/tabs with visible escape sequences by default.
    - Removes remaining C0 control characters and DEL.
    """
    text = "" if value is None else str(value)
    # Normalize line endings early.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if keep_newlines:
        text = text.replace("\t", "\\t")
    else:
        text = text.replace("\n", "\\n").replace("\t", "\\t")

    text = strip_ansi(text)

    # Drop remaining control chars (keep \n only if requested).
    out_chars = []
    for ch in text:
        o = ord(ch)
        if keep_newlines and ch == "\n":
            out_chars.append(ch)
            continue
        if o < 0x20 or o == 0x7F:
            continue
        out_chars.append(ch)
    return "".join(out_chars)


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


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
        safe_key = sanitize_for_terminal(key)
        plain_key_str = f"│ {safe_key}: "
        plain_indent = "│   "

        # Colored strings for printing
        colored_key_str = f"{c_start}│{c_end} {safe_key}: "
        colored_indent = f"{c_start}│{c_end}   "

        # Format complex values
        if isinstance(value, (dict, list)):
            val_str = pprint.pformat(value, width=content_width - len(plain_indent))
        else:
            val_str = value

        safe_val_str = sanitize_for_terminal(val_str)

        # Wrap long text
        wrapped_lines = textwrap.wrap(
            safe_val_str, width=content_width - len(plain_key_str) + len(plain_indent)
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


class Spinner:
    """A context manager that displays a spinner animation."""

    def __init__(self, message: str = "Loading...", delay: float = 0.1):
        self.message = message
        self.delay = delay
        self.stop_running = False
        self.spinner_thread = None

    def spin(self):
        spinner_chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
        while not self.stop_running:
            sys.stdout.write(f"\r{next(spinner_chars)} {self.message}")
            sys.stdout.flush()
            time.sleep(self.delay)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.stop_running = False
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def stop(self):
        self.stop_running = True
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()

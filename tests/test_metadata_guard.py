from pathlib import Path

import pytest

from scripts import metadata_guard


VALID_FRONT_MATTER = """---
title: Example Title
summary: Short summary.
tags:
  - example
status: active
created: 2025-05-05
updated: 2025-05-05
---

# Heading

Body text.
"""


def write_markdown(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def test_valid_file_passes(tmp_path: Path) -> None:
    file_path = write_markdown(tmp_path, "example-file.md", VALID_FRONT_MATTER)
    errors = metadata_guard.run([file_path])
    assert errors == []


def test_missing_front_matter_fails(tmp_path: Path) -> None:
    file_path = write_markdown(tmp_path, "example-file.md", "# Missing metadata\n")
    errors = metadata_guard.run([file_path])
    assert any("missing YAML front matter" in error.message for error in errors)


def test_invalid_filename_flagged(tmp_path: Path) -> None:
    file_path = write_markdown(tmp_path, "Invalid.md", VALID_FRONT_MATTER)
    errors = metadata_guard.run([file_path])
    assert any("file name must be lower-case kebab-case" in error.message for error in errors)


def test_tags_must_be_list(tmp_path: Path) -> None:
    content = VALID_FRONT_MATTER.replace("tags:\n  - example", "tags: not-a-list")
    file_path = write_markdown(tmp_path, "example-file.md", content)
    errors = metadata_guard.run([file_path])
    assert any("tags must be a list" in error.message for error in errors)

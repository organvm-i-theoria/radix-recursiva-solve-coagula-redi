"""Validate documentation naming conventions and front matter metadata."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

FRONT_MATTER_BOUNDARY = re.compile(r"^---\s*$")
FILENAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
REQUIRED_KEYS = ("title", "summary", "tags", "status")
VALID_STATUS = {"draft", "active", "deprecated", "archived"}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class ValidationError:
    path: Path
    message: str

    def format(self) -> str:
        return f"{self.path.as_posix()}: {self.message}"


def discover_markdown_files(paths: Sequence[Path]) -> Iterable[Path]:
    for base in paths:
        if base.is_file() and base.suffix == ".md":
            yield base
        elif base.is_dir():
            for path in base.rglob("*.md"):
                if path.is_file():
                    yield path


def validate_filename(path: Path) -> List[ValidationError]:
    name = path.name
    if name.lower() in {"readme.md", "license.md"}:
        return []
    if not FILENAME_PATTERN.match(name):
        return [
            ValidationError(
                path, "file name must be lower-case kebab-case (e.g., example-file.md)"
            )
        ]
    return []


def split_front_matter(content: str) -> tuple[str, str] | tuple[None, None]:
    lines = content.splitlines()
    if not lines or not FRONT_MATTER_BOUNDARY.match(lines[0]):
        return None, None
    for index in range(1, len(lines)):
        if FRONT_MATTER_BOUNDARY.match(lines[index]):
            metadata = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1 :])
            return metadata, body
    return None, None


def parse_front_matter(
    block: str, path: Path
) -> tuple[dict[str, object], List[ValidationError]]:
    data: dict[str, object] = {}
    errors: list[ValidationError] = []
    current_key: str | None = None

    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - "):
            if current_key is None:
                errors.append(
                    ValidationError(
                        path, f"unexpected list item without key: '{line.strip()}'"
                    )
                )
                continue
            value = data.setdefault(current_key, [])
            if not isinstance(value, list):
                errors.append(
                    ValidationError(
                        path, f"key '{current_key}' does not accept list items"
                    )
                )
                continue
            value.append(line[4:].strip())
            continue
        if line.startswith("  "):
            if current_key is None or not isinstance(data.get(current_key), str):
                errors.append(
                    ValidationError(
                        path, f"unexpected continuation line: '{line.strip()}'"
                    )
                )
                continue
            data[current_key] = f"{data[current_key]}\n{line.strip()}"
            continue
        if ":" not in line:
            errors.append(ValidationError(path, f"malformed metadata line: '{line}'"))
            current_key = None
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            errors.append(ValidationError(path, "metadata key cannot be empty"))
            current_key = None
            continue
        if not value:
            data[key] = []
            current_key = key
            continue
        data[key] = value
        current_key = key

    return data, errors


def validate_front_matter(data: dict[str, object], path: Path) -> List[ValidationError]:
    errors: List[ValidationError] = []

    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(
                ValidationError(path, f"missing required metadata key '{key}'")
            )

    status = data.get("status")
    if isinstance(status, str):
        if status not in VALID_STATUS:
            errors.append(
                ValidationError(path, f"status must be one of {sorted(VALID_STATUS)}")
            )
    elif status is not None:
        errors.append(ValidationError(path, "status must be a string"))

    summary = data.get("summary")
    if isinstance(summary, str) and len(summary) > 200:
        errors.append(
            ValidationError(path, "summary should be 200 characters or fewer")
        )
    elif summary is not None and not isinstance(summary, str):
        errors.append(ValidationError(path, "summary must be a string"))

    title = data.get("title")
    if title is None:
        pass
    elif not isinstance(title, str) or not title.strip():
        errors.append(ValidationError(path, "title must be a non-empty string"))

    tags = data.get("tags")
    if isinstance(tags, list):
        if not tags:
            errors.append(ValidationError(path, "tags list cannot be empty"))
        for tag in tags:
            if not isinstance(tag, str) or not re.fullmatch(
                r"[a-z0-9]+(?:-[a-z0-9]+)*", tag
            ):
                errors.append(
                    ValidationError(path, f"tag '{tag}' must be lower-case kebab-case")
                )
    elif tags is not None:
        errors.append(ValidationError(path, "tags must be a list"))

    for key in ("created", "updated"):
        value = data.get(key)
        if value is None:
            continue
        if not isinstance(value, str) or not DATE_PATTERN.match(value):
            errors.append(
                ValidationError(path, f"{key} must use ISO format YYYY-MM-DD")
            )

    return errors


def validate_file(path: Path) -> List[ValidationError]:
    errors = validate_filename(path)
    content = path.read_text(encoding="utf-8")
    metadata_block, body = split_front_matter(content)
    if metadata_block is None:
        errors.append(ValidationError(path, "missing YAML front matter"))
        return errors
    data, parse_errors = parse_front_matter(metadata_block, path)
    errors.extend(parse_errors)
    errors.extend(validate_front_matter(data, path))

    if body and body.lstrip().startswith("# "):
        pass
    else:
        errors.append(
            ValidationError(
                path, "body should start with an H1 heading after the front matter"
            )
        )

    return errors


def run(paths: Sequence[Path]) -> List[ValidationError]:
    markdown_files = sorted({path for path in discover_markdown_files(paths)})
    errors: List[ValidationError] = []
    for file_path in markdown_files:
        errors.extend(validate_file(file_path))
    return errors


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("docs")],
        help="Directories or markdown files to validate (default: docs)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    errors = run(args.paths)
    if errors:
        for error in errors:
            print(error.format())
        return 1
    print("All documentation metadata checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

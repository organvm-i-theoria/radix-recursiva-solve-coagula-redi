"""Generate lightweight AI-assisted review notes for Markdown changes.

The initial helper focused on summarising Markdown diffs. This revision expands the
logic to include:

* Defensive guards around diff discovery and file reading so that deleted or
  renamed files do not abort the run.
* Additional readability diagnostics and flags that highlight potentially dense
  prose or unusually long sentences which can be blind spots during reviews.
* More exhaustive reporting, including explicit notes when content is empty,
  binary, or otherwise unsuitable for summarisation.

The goal is to keep the helper open-source while making the resulting report more
actionable for reviewers who rely on it as a second pair of eyes.
"""
from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

import textstat  # type: ignore
from sumy.nlp.tokenizers import Tokenizer  # type: ignore
from sumy.parsers.plaintext import PlaintextParser  # type: ignore
from sumy.summarizers.lsa import LsaSummarizer  # type: ignore


MAX_SUMMARY_SENTENCES = 3
MIN_CONTENT_THRESHOLD = 20


@dataclass
class ReadabilitySnapshot:
    """Captured readability metrics and qualitative flags for a text sample."""

    sentence_count: int
    flesch_ease: float
    grade_level: str
    red_flags: Sequence[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI-assisted Markdown reviewer")
    parser.add_argument("--base", required=True, help="Base commit or ref for diff")
    parser.add_argument("--head", required=True, help="Head commit or ref for diff")
    parser.add_argument(
        "--output",
        default="ai_review_report.md",
        help="Path to write the generated review report",
    )
    parser.add_argument(
        "--include",
        nargs="*",
        default=[".md", ".mdx"],
        help="File extensions to analyse",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=1200,
        help="Maximum number of characters from each file to summarise",
    )
    return parser.parse_args()


def git_diff_files(base: str, head: str) -> List[str]:
    """Return files that differ between two refs.

    The subprocess invocation can raise ``CalledProcessError`` if either ref is
    missing. We catch that at the call site to ensure the report still renders a
    useful diagnostic instead of crashing the workflow.
    """

    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Unable to compute git diff")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def filter_files(paths: Iterable[str], exts: Iterable[str]) -> List[Path]:
    ext_set = {ext.lower() for ext in exts}
    return [Path(p) for p in paths if Path(p).suffix.lower() in ext_set]


def safe_read_text(path: Path) -> tuple[str, str | None]:
    """Read file content defensively.

    Returns a tuple of ``(text, error_message)`` where ``error_message`` is ``None``
    when the read succeeded. We treat empty strings as valid input so the caller
    can differentiate between "no content" and "failed to load".
    """

    if not path.exists():
        return "", "File no longer exists in the checked-out workspace."

    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        return "", "File is not UTF-8 text."
    except OSError as exc:  # pragma: no cover - exercised in workflow
        return "", f"Unable to read file: {exc}"  # pragma: no cover


def summarise_text(text: str, summariser: LsaSummarizer, max_chars: int) -> str:
    chunk = text[:max_chars]
    if not chunk.strip():
        return "No substantive content detected."

    try:
        parser = PlaintextParser.from_string(chunk, Tokenizer("english"))
    except LookupError:
        return "Tokenizer resources missing: install NLTK 'punkt' data to enable summaries."
    except ValueError:
        return "Unable to parse content for summarisation."

    total_sentences = len(list(parser.document.sentences))
    if total_sentences == 0:
        return "No sentences available for summarisation."

    sentences_to_return = max(1, min(MAX_SUMMARY_SENTENCES, total_sentences))
    try:
        summary_sentences = summariser(parser.document, sentences_count=sentences_to_return)
    except LookupError:
        return "Summariser resources missing: install NLTK 'punkt' data to enable summaries."

    summary = " ".join(str(sentence).strip() for sentence in summary_sentences).strip()
    if summary:
        return summary
    return "Unable to generate summary from the available text."


def analyse_readability(text: str) -> ReadabilitySnapshot:
    if not text.strip():
        return ReadabilitySnapshot(0, 0.0, "Unavailable", ("No content to analyse.",))

    sentences = textstat.sentence_count(text) or 1
    flesch = float(textstat.flesch_reading_ease(text))
    grade = textstat.text_standard(text, float_output=False)

    flags: list[str] = []
    avg_sentence_length = textstat.avg_sentence_length(text)
    if flesch < 50:
        flags.append("Dense reading: consider shorter sentences or simpler vocabulary.")
    if avg_sentence_length > 25:
        flags.append("Long sentences detected: aim for < 25 words where possible.")
    if sentences < 3 and len(text) > MIN_CONTENT_THRESHOLD:
        flags.append("Large blocks of text with few sentence breaks.")

    return ReadabilitySnapshot(sentences, flesch, grade, tuple(flags))


def readability_report(snapshot: ReadabilitySnapshot) -> str:
    lines = [
        f"- Sentences analysed: {snapshot.sentence_count}",
        f"- Flesch reading ease: {snapshot.flesch_ease:.2f}",
        f"- Estimated grade level: {snapshot.grade_level}",
    ]
    if snapshot.red_flags:
        lines.append("- Flags:")
        lines.extend(f"  - {flag}" for flag in snapshot.red_flags)
    else:
        lines.append("- Flags: None detected")
    return "\n".join(lines)


def build_report(base: str, head: str, include: Iterable[str], max_chars: int, output: Path) -> None:
    lines = ["# AI Review Summary", ""]
    lines.append(f"Compared commits `{base}` → `{head}`.")
    lines.append("")

    try:
        diffed_files = git_diff_files(base, head)
    except RuntimeError as exc:
        lines.append("Unable to enumerate changes.")
        lines.append("")
        lines.append(f"``{str(exc) or 'Unknown git error.'}``")
        output.write_text("\n".join(lines), encoding="utf-8")
        return

    changed_files = filter_files(diffed_files, include)
    summariser = LsaSummarizer()

    if not changed_files:
        lines.append("No matching files changed.")
    else:
        for path in changed_files:
            lines.append(f"## {path}")
            lines.append("")

            content, error = safe_read_text(path)
            if error:
                lines.append("### Unable to analyse file")
                lines.append("")
                lines.append(error)
                lines.append("")
                continue

            lines.append("### AI Summary")
            lines.append("")
            lines.append(summarise_text(content, summariser, max_chars))
            lines.append("")
            lines.append("### Readability metrics")
            lines.append("")
            snapshot = analyse_readability(content)
            lines.append(readability_report(snapshot))
            lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    args = parse_args()
    build_report(args.base, args.head, args.include, args.max_chars, Path(args.output))

"""Unit tests for the AI reviewer helper."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

sumy_module = pytest.importorskip("sumy")
from sumy.summarizers.lsa import LsaSummarizer  # noqa: E402

import scripts.ai_reviewer as reviewer


def test_summarise_text_handles_empty_content() -> None:
    summariser = LsaSummarizer()
    result = reviewer.summarise_text("", summariser, max_chars=200)
    assert "No substantive content" in result


def test_summarise_text_returns_sentences() -> None:
    summariser = LsaSummarizer()
    text = (
        "This helper reviews Markdown files. "
        "It highlights readability concerns. "
        "Summaries should remain concise."
    )
    result = reviewer.summarise_text(text, summariser, max_chars=200)
    assert result, "Summarisation should return a non-empty message"


def test_analyse_readability_flags_dense_text() -> None:
    dense_text = " ".join(["This sentence contains numerous polysyllabic expressions." for _ in range(5)])
    snapshot = reviewer.analyse_readability(dense_text)
    assert snapshot.red_flags, "Expected readability flags for dense text"


def test_build_report_handles_git_errors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    output = tmp_path / "report.md"

    def fake_git_diff(base: str, head: str) -> list[str]:  # noqa: ARG001 - required signature
        raise RuntimeError("diff failed")

    monkeypatch.setattr(reviewer, "git_diff_files", fake_git_diff)

    reviewer.build_report("base", "head", [".md"], max_chars=200, output=output)

    content = output.read_text(encoding="utf-8")
    assert "diff failed" in content


def test_build_report_includes_readability_section(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    output = tmp_path / "report.md"
    monkeypatch.setattr(reviewer, "git_diff_files", lambda base, head: ["sample.md"])  # noqa: ARG005
    monkeypatch.setattr(
        reviewer,
        "safe_read_text",
        lambda path: ("Short text. Another sentence here.", None),
    )

    reviewer.build_report("base", "head", [".md"], max_chars=200, output=output)

    content = output.read_text(encoding="utf-8")
    assert "### Readability metrics" in content
    assert "Flesch reading ease" in content

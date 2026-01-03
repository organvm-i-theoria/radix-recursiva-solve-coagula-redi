"""Repository audit utilities for thread digests and protocol keywords."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

OUTPUT_FILE = Path('thread_protocol_index.csv')
KEYWORD_REPORT = Path('keyword_matches.csv')
WALK_REPORT = Path('walk_report.csv')
IGNORE = {'walk_report.csv'}
DEFAULT_KEYWORDS = ["protocol", "SOP", "process", "naming"]


def find_thread_files() -> list[Path]:
    """Return all markdown or CSV files containing "THREAD" in their name."""
    patterns = ["*THREAD*.md", "*THREAD*.csv"]
    files = set()
    for pattern in patterns:
        files.update(Path('.').rglob(pattern))
    return sorted(p for p in files if p.resolve() != OUTPUT_FILE.resolve())


def parse_markdown_table(file_path: Path) -> list[dict]:
    rows = []
    with file_path.open('r', encoding='utf-8') as handle:
        for line in handle:
            line = line.strip()
            if not line.startswith('| TH'):
                continue
            parts = [segment.strip() for segment in line.strip('|').split('|')]
            if len(parts) < 3:
                continue
            rows.append(
                {
                    'thread_id': parts[0],
                    'title': parts[1],
                    'timestamp': parts[2],
                    'source_file': str(file_path),
                }
            )
    return rows


def parse_csv_table(file_path: Path) -> list[dict]:
    rows = []
    with file_path.open(newline='', encoding='utf-8') as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for row in reader:
            if not row or not row[0].startswith('TH'):
                continue
            title = row[1] if len(row) > 1 else ''
            timestamp = row[2] if len(row) > 2 else ''
            rows.append(
                {
                    'thread_id': row[0],
                    'title': title,
                    'timestamp': timestamp,
                    'source_file': str(file_path),
                }
            )
    return rows


def build_index() -> None:
    rows = []
    for file_path in find_thread_files():
        suffix = file_path.suffix.lower()
        if suffix == '.md':
            rows.extend(parse_markdown_table(file_path))
        elif suffix == '.csv':
            rows.extend(parse_csv_table(file_path))
    rows.sort(key=lambda entry: (entry['thread_id'], entry['source_file']))
    with OUTPUT_FILE.open('w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['thread_id', 'title', 'timestamp', 'source_file']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _match_keyword(title: str, keywords: Iterable[str]) -> Optional[str]:
    lower_title = title.lower()
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in lower_title:
            return kw_lower
    return None


def _scan_file(path: Path, keywords: Iterable[str]) -> List[Tuple[str, str, str, str]]:
    row_re = re.compile(r"^\|\s*(TH\d+)\s*\|\s*([^|]+?)\s*\|")
    matches: List[Tuple[str, str, str, str]] = []
    with path.open('r', encoding='utf-8') as handle:
        for line in handle:
            match = row_re.match(line)
            if not match:
                continue
            thread_id, title = match.groups()
            kw = _match_keyword(title, keywords)
            if kw:
                matches.append((thread_id, str(path), title.strip(), kw))
    return matches


def scan_digests(
    digest_dir: Path,
    report_path: Path,
    keywords: Iterable[str],
) -> None:
    """
    Scan digest files for thread entries matching keywords and write to CSV report.
    
    Output CSV schema:
    - thread_id: Thread identifier (e.g., TH195)
    - digest_path: Path to the digest markdown file
    - title: Thread title text
    - keyword: Matched keyword from the search list
    """
    digest_files = sorted(digest_dir.glob('PR*_THREAD_DIGEST.md'))
    matches: List[Tuple[str, str, str, str]] = []
    for path in digest_files:
        matches.extend(_scan_file(path, keywords))

    existing = set()
    if report_path.exists():
        with report_path.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing.add((row['thread_id'], row['digest_path']))

    write_header = not report_path.exists()
    with report_path.open('a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['thread_id', 'digest_path', 'title', 'keyword']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for thread_id, dpath, title, keyword in matches:
            key = (thread_id, dpath)
            if key not in existing:
                writer.writerow(
                    {
                        'thread_id': thread_id,
                        'digest_path': dpath,
                        'title': title,
                        'keyword': keyword,
                    }
                )
                existing.add(key)


def analyze(root: str = '.') -> tuple[list[dict], int]:
    root_path = Path(root).resolve()
    report: list[dict] = []
    max_depth = 0
    # Pre-compute lowercased keywords to avoid redundant operations
    lower_keywords = [kw.lower() for kw in DEFAULT_KEYWORDS]

    def update_depth(depth: int) -> None:
        nonlocal max_depth
        if depth > max_depth:
            max_depth = depth

    def handle_file(display_path: str, name: str, data: bytes, depth: int) -> None:
        name_lower = name.lower()
        name_matches = [kw for kw, kw_lower in zip(DEFAULT_KEYWORDS, lower_keywords) if kw_lower in name_lower]
        text = data.decode('utf-8', errors='ignore').lower()
        content_matches = [kw for kw, kw_lower in zip(DEFAULT_KEYWORDS, lower_keywords) if kw_lower in text]
        mismatch = sorted(set(name_matches) ^ set(content_matches))
        sha256 = hashlib.sha256(data).hexdigest()
        report.append(
            {
                'path': display_path,
                'name_matches': ';'.join(name_matches),
                'content_matches': ';'.join(content_matches),
                'mismatch': ';'.join(mismatch),
                'sha256': sha256,
            }
        )
        update_depth(depth)

    def scan_zip(zf: zipfile.ZipFile, base: str, base_depth: int) -> None:
        for info in zf.infolist():
            if info.is_dir():
                continue
            data = zf.read(info.filename)
            inner_path = f"{base}!{info.filename}"
            inner_depth = base_depth + len(Path(info.filename).parts)
            handle_file(inner_path, info.filename, data, inner_depth)
            if info.filename.lower().endswith('.zip'):
                with zipfile.ZipFile(BytesIO(data)) as inner_zip:
                    scan_zip(inner_zip, inner_path, inner_depth)

    for path in root_path.rglob('*'):
        if path.name in IGNORE or not path.is_file():
            continue
        rel_path = path.relative_to(root_path)
        depth = len(rel_path.parts)
        if path.suffix.lower() == '.zip':
            try:
                with zipfile.ZipFile(path) as zf:
                    scan_zip(zf, str(rel_path), depth)
            except zipfile.BadZipFile:
                handle_file(str(rel_path), path.name, path.read_bytes(), depth)
        else:
            handle_file(str(rel_path), path.name, path.read_bytes(), depth)

    return report, max_depth


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit thread digests and protocol keyword usage.",
    )
    parser.add_argument(
        '--digest-dir',
        default='ARCHIVAL_STACK',
        help='Directory containing digest files',
    )
    parser.add_argument(
        '--report',
        default=str(KEYWORD_REPORT),
        help='CSV file to append keyword matches to',
    )
    parser.add_argument(
        '--keywords',
        default=','.join(DEFAULT_KEYWORDS),
        help='Comma-separated list of keywords to search for',
    )
    parser.add_argument(
        '--skip-index',
        action='store_true',
        help='Skip building the thread protocol index',
    )
    parser.add_argument(
        '--skip-walk',
        action='store_true',
        help='Skip generating the repository walk report',
    )
    args = parser.parse_args()

    keywords = [kw.strip() for kw in args.keywords.split(',') if kw.strip()]
    scan_digests(Path(args.digest_dir), Path(args.report), keywords)

    if not args.skip_index:
        build_index()
    if not args.skip_walk:
        rows, max_depth = analyze('.')
        with WALK_REPORT.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=['path', 'name_matches', 'content_matches', 'mismatch', 'sha256'],
            )
            writer.writeheader()
            writer.writerows(rows)
        print(f'Max depth: {max_depth}')
        print(f'Wrote {len(rows)} entries to {WALK_REPORT}')

    if not args.skip_index:
        print(f'Wrote {OUTPUT_FILE}')
    if args.report:
        print(f'Updated {args.report}')


if __name__ == '__main__':
    main()

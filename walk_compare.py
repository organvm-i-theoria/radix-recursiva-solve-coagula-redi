import csv
import hashlib
from io import BytesIO
from pathlib import Path
import zipfile

KEYWORDS = ['protocol', 'sop', 'naming', 'process']
IGNORE = {'walk_report.csv'}

def analyze(root='.'):
    root_path = Path(root).resolve()
    report = []
    max_depth = [0]  # mutable holder

    def update_depth(depth: int) -> None:
        if depth > max_depth[0]:
            max_depth[0] = depth

    def handle_file(display_path: str, name: str, data: bytes, depth: int) -> None:
        name_lower = name.lower()
        name_matches = [kw for kw in KEYWORDS if kw in name_lower]
        text = data.decode('utf-8', errors='ignore').lower()
        content_matches = [kw for kw in KEYWORDS if kw in text]
        mismatch = sorted(set(name_matches) ^ set(content_matches))
        sha256 = hashlib.sha256(data).hexdigest()
        report.append({
            'path': display_path,
            'name_matches': ';'.join(name_matches),
            'content_matches': ';'.join(content_matches),
            'mismatch': ';'.join(mismatch),
            'sha256': sha256,
        })
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
                data = path.read_bytes()
                handle_file(str(rel_path), path.name, data, depth)
        else:
            data = path.read_bytes()
            handle_file(str(rel_path), path.name, data, depth)

    return report, max_depth[0]

def main() -> None:
    report, max_depth = analyze('.')
    print(f'Max depth: {max_depth}')
    out_file = Path('walk_report.csv')
    with out_file.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['path', 'name_matches', 'content_matches', 'mismatch', 'sha256'],
            lineterminator='\n',
        )
        writer.writeheader()
        writer.writerows(report)
    print(f'Wrote {len(report)} entries to {out_file}')
import glob
from pathlib import Path

# Files to parse
CROSSWALK_FILE = Path('THREAD_PROJECT_CROSSWALK.md')
DIGEST_GLOB = 'ARCHIVAL_STACK/PR*_THREAD_DIGEST.md'
OUTPUT_FILE = Path('thread_protocol_index.csv')

def parse_markdown_table(file_path):
    """Parse markdown table rows for thread entries.

    Expects rows formatted like:
    | THxxx | Title | timestamp | ... |
    Returns list of dicts with thread_id, title, timestamp.
    """
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('| TH'):
                # remove leading/trailing '|'
                parts = [p.strip() for p in line.strip('|').split('|')]
                if len(parts) >= 3:
                    rows.append({
                        'thread_id': parts[0],
                        'title': parts[1],
                        'timestamp': parts[2],
                        'source_file': str(file_path)
                    })
    return rows

def build_index():
    rows = []
    # parse crosswalk
    if CROSSWALK_FILE.exists():
        rows.extend(parse_markdown_table(CROSSWALK_FILE))
    # parse digest files
    for digest_file in sorted(glob.glob(DIGEST_GLOB)):
        rows.extend(parse_markdown_table(Path(digest_file)))
    # write CSV
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['thread_id', 'title', 'timestamp', 'source_file']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    build_index()
    print(f"Wrote {OUTPUT_FILE}")

if __name__ == '__main__':
    main()

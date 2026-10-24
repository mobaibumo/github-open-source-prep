"""Read-only, bounded project inventory. Not a secret scanner or Git history audit."""
import argparse
import json
import os
from pathlib import Path
import re

SKIP = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.next', '.cache'}
SECRET = re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\bgh[pousr]_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b')
DESIGN = {'.psd', '.ai', '.blend', '.sketch', '.fig', '.step', '.stp', '.cad'}
IMAGE = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.tif', '.tiff', '.exr'}


def inspect(root, max_files=20000, large_bytes=20 * 1024 * 1024):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Project path must be a directory')
    result = {'root': str(root), 'files_seen': 0, 'bytes_seen': 0,
              'types': [], 'findings': [], 'skipped_directories': [],
              'truncated': False, 'limitations': [
                  'Does not inspect Git status, tracked files, ignored rules or commit history.',
                  'Only selected credential patterns are detected; absence of findings is not clearance.',
                  'Content inspection is limited to files up to 1 MiB; binary files are not decoded.',
                  'Symlinks, junctions and common dependency/cache directories are skipped.']}
    types = set()

    def finding(path, kind):
        result['findings'].append({'path': path, 'kind': kind})

    def error(exc):
        finding('unreadable-directory', type(exc).__name__)

    for directory, dirs, files in os.walk(root, followlinks=False, onerror=error):
        parent = Path(directory)
        keep = []
        for name in sorted(dirs):
            path = parent / name
            rel = path.relative_to(root).as_posix()
            if name in SKIP or path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
                result['skipped_directories'].append(rel)
            elif (path / '.git').exists():
                finding(rel, 'nested-repository-skipped')
            else:
                keep.append(name)
        dirs[:] = keep
        for name in sorted(files):
            if result['files_seen'] >= max_files:
                result['truncated'] = True
                result['types'] = sorted(types)
                return result
            path = parent / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                finding(rel, 'symlink-skipped')
                continue
            try:
                size = path.stat().st_size
                result['files_seen'] += 1
                result['bytes_seen'] += size
                suffix = path.suffix.lower()
                if name == 'SKILL.md':
                    types.add('skill')
                if name in {'package.json', 'pyproject.toml', 'requirements.txt', 'Cargo.toml', 'go.mod', 'pom.xml', 'CMakeLists.txt'} or suffix in {'.py', '.js', '.ts', '.go', '.rs', '.java', '.cs'}:
                    types.add('code')
                if suffix in DESIGN:
                    types.add('design-assets')
                    finding(rel, 'editable-source-review-upload-scope')
                if suffix in IMAGE:
                    types.add('images')
                if size >= large_bytes:
                    finding(rel, 'large-file-review')
                if (name == '.env' or name.startswith('.env.')) and not name.endswith(('.example', '.sample', '.template')):
                    finding(rel, 'environment-file-review')
                if suffix in {'.pem', '.key', '.p12', '.pfx'} or name in {'id_rsa', 'id_ed25519', '.npmrc', '.pypirc'}:
                    finding(rel, 'credential-file-review')
                if size <= 1024 * 1024:
                    data = path.read_bytes()
                    if SECRET.search(data):
                        finding(rel, 'credential-pattern-review')
            except OSError as exc:
                finding(rel, 'unreadable-file-' + type(exc).__name__)
    result['types'] = sorted(types) or ['unclassified']
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    parser.add_argument('--max-files', type=int, default=20000)
    parser.add_argument('--large-mib', type=int, default=20)
    args = parser.parse_args()
    if args.max_files <= 0 or args.large_mib <= 0:
        parser.error('Limits must be positive')
    try:
        report = inspect(args.path, args.max_files, args.large_mib * 1024 * 1024)
    except (OSError, ValueError) as exc:
        parser.exit(2, 'Cannot inspect project: ' + type(exc).__name__ + '\n')
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()

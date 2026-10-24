"""Isolated smoke checks; does not use a live repository or network."""
import json
from pathlib import Path
import tempfile
from inspect_project import inspect


with tempfile.TemporaryDirectory(prefix='project-inspector-') as directory:
    root = Path(directory)
    (root / 'SKILL.md').write_text('example', encoding='utf-8')
    (root / 'main.py').write_text('print(1)', encoding='utf-8')
    (root / '.env').write_text('TOKEN=example', encoding='utf-8')
    marker = 'ghp_' + 'a' * 30
    (root / 'credential.txt').write_text(marker, encoding='utf-8')
    (root / 'preview.png').write_bytes(b'preview')
    (root / 'original.psd').write_bytes(b'original')
    (root / 'node_modules').mkdir()
    (root / 'node_modules' / 'hidden.txt').write_text(marker)
    (root / 'nested').mkdir()
    (root / 'nested' / '.git').mkdir()
    before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
    report = inspect(root, large_bytes=5)
    assert set(report['types']) == {'skill', 'code', 'images', 'design-assets'}
    assert marker not in json.dumps(report)
    assert any(f['kind'] == 'credential-pattern-review' for f in report['findings'])
    assert any(f['kind'] == 'environment-file-review' for f in report['findings'])
    assert any(f['kind'] == 'nested-repository-skipped' for f in report['findings'])
    assert 'node_modules' in report['skipped_directories']
    assert inspect(root, max_files=1)['truncated']
    after = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
    assert before == after, 'Inspector changed fixture files'
print('PASS: mixed types, redaction, exclusions, limits and read-only behavior')

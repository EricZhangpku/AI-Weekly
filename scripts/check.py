#!/usr/bin/env python3
"""Check generated internal paths, fragments and duplicate IDs before publishing."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]/'site'
class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.refs = set(), []
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for attr in ('href','src'):
            if attrs.get(attr): self.refs.append(attrs[attr])

docs = {p:Document(p) for p in ROOT.rglob('*.html')}
assert ROOT/'index.html' in docs, 'Missing homepage'
assert any(p.parent.name == 'issues' for p in docs), 'Missing issue pages'
refs = 0
for path, doc in docs.items():
    for ref in doc.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        target = (path.parent/unquote(url.path)).resolve() if url.path else path
        if target.is_dir(): target /= 'index.html'
        assert target.is_relative_to(ROOT), f'Escaped site: {path}: {ref}'
        assert target.exists(), f'Missing file: {path}: {ref}'
        if url.fragment and target in docs:
            assert unquote(url.fragment) in docs[target].ids, f'Missing anchor: {path}: {ref}'
        refs += 1
print(f'OK: {len(docs)} pages, {refs} local links/assets/fragments; no duplicate IDs.')

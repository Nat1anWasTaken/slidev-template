#!/usr/bin/env python3
"""Subset Noto Sans TC / Noto Serif TC to the glyphs the deck actually uses.

Google Sans has no CJK glyphs, so the theme self-hosts two small WOFF2 subsets
(see theme/styles/cjk.css). They are committed, so CI and offline machines need
nothing extra. Re-run this script whenever on-slide Chinese text changes:

    pnpm fonts            # rebuild both subsets (needs uv; downloads sources once)
    pnpm fonts:check      # plain python3: list characters missing from the subsets

Equivalent without pnpm:

    uv run --with fonttools --with brotli python scripts/subset-fonts.py
    python3 scripts/subset-fonts.py --check

What gets scanned: slides.md, pages/**/*.md, layouts/components in theme/ and
the repo root, and JSON data files in data/. Presenter notes
(HTML comments in .md files) are skipped because they are not rendered with the
slide fonts; pass --include-notes to keep them. Extra files can be passed as
arguments (e.g. a scratch deck: `pnpm fonts slides-demo.md`).

Sources are the variable TTFs from google/fonts, pinned to a commit and cached in
$DECK_FONT_CACHE (default ~/.cache/slidev-google-theme/fonts, shared by every deck). Both fonts are
licensed under the SIL Open Font License 1.1 (theme/assets/fonts/OFL-NotoTC.txt).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / 'theme' / 'assets' / 'fonts'
GLYPH_LIST = OUT_DIR / 'cjk-glyphs.txt'

SOURCES = {
    'sans': {
        'url': 'https://raw.githubusercontent.com/google/fonts/3be1884c48c3e45b52ecc725676a08f87776373e/ofl/notosanstc/NotoSansTC%5Bwght%5D.ttf',
        'file': 'NotoSansTC[wght].ttf',
        'sha256': '864727d210d54f2537bbe23b3a839436c3992af72de9322af5270897246bd44f',
        'out': 'NotoSansTC-subset.woff2',
        # Keep the weight axis, limited to the weights the theme uses (400-700).
        'wght': (400, 700),
    },
    'serif': {
        'url': 'https://raw.githubusercontent.com/google/fonts/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/notoseriftc/NotoSerifTC%5Bwght%5D.ttf',
        'file': 'NotoSerifTC[wght].ttf',
        'sha256': '0077e18f57c6908f4a000969880940bdb0dad057c0e8d98b49dc364c3d1b09c6',
        'out': 'NotoSerifTC-subset.woff2',
        # Serif is for quotes; one static weight is much smaller than the variable font.
        'wght': 500,
    },
}

SCAN_GLOBS = [
    'slides.md',
    'pages/**/*.md',
    'theme/layouts/*.vue',
    'theme/components/*.vue',
    'layouts/*.vue',
    'components/**/*.vue',
    'data/*.json',
]

# Always included: printable ASCII plus common CJK punctuation and symbols, so
# small edits (a new comma, a date) never fall back to a system font.
BASE = ''.join(chr(c) for c in range(0x20, 0x7F)) + (
    '　、。，．：；！？「」『』《》〈〉（）［］【】〔〕'
    '…‥—–～·・／＼％＋－＝×÷°℃'
    '０１２３４５６７８９'
    '←→↑↓○●◎◇◆□■△▲☆★'
    '“”‘’©'
    '一二三四五六七八九十百千年月日時分'
)

COMMENT_RE = re.compile(r'<!--.*?-->', re.S)


def cache_dir() -> Path:
    env = os.environ.get('DECK_FONT_CACHE')
    base = Path(env) if env else Path.home() / '.cache' / 'slidev-google-theme' / 'fonts'
    base.mkdir(parents=True, exist_ok=True)
    return base


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def fetch(src: dict) -> Path:
    path = cache_dir() / src['file']
    if path.exists() and sha256(path) == src['sha256']:
        return path
    print(f"downloading {src['file']} ...", file=sys.stderr)
    tmp = path.with_suffix('.part')
    urllib.request.urlretrieve(src['url'], tmp)
    digest = sha256(tmp)
    if digest != src['sha256']:
        tmp.unlink()
        raise SystemExit(f"checksum mismatch for {src['file']}: {digest}")
    tmp.replace(path)
    return path


def scan(extra: list[str], include_notes: bool) -> tuple[set[str], list[Path]]:
    files: list[Path] = []
    for pattern in SCAN_GLOBS:
        files.extend(sorted(ROOT.glob(pattern)))
    for name in extra:
        p = Path(name)
        files.append(p if p.is_absolute() else (Path.cwd() / p))
    chars = set(BASE)
    for f in files:
        text = f.read_text(encoding='utf-8')
        if f.suffix == '.md' and not include_notes:
            text = COMMENT_RE.sub('', text)
        chars.update(c for c in text if c.isprintable() or c == '　')
    return chars, files


def check(chars: set[str]) -> int:
    if not GLYPH_LIST.exists():
        print('no glyph list yet; run `pnpm fonts` first', file=sys.stderr)
        return 1
    have = set(GLYPH_LIST.read_text(encoding='utf-8'))
    missing = sorted(c for c in chars if c not in have)
    if missing:
        print(f"{len(missing)} character(s) missing from the font subsets: {''.join(missing)}")
        print('run `pnpm fonts` to rebuild them')
        return 1
    print(f'font subsets cover all {len(chars)} characters in use')
    return 0


def build(chars: set[str]) -> None:
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    text = ''.join(sorted(chars))
    for key, src in SOURCES.items():
        font = TTFont(fetch(src))
        opts = subset.Options()
        opts.flavor = 'woff2'
        opts.layout_features = ['*']  # keep vert/vrt2 (vertical text), palt, locl...
        opts.name_IDs = ['*']
        opts.hinting = False
        opts.notdef_outline = True
        subsetter = subset.Subsetter(opts)
        subsetter.populate(text=text)
        subsetter.subset(font)
        font = instancer.instantiateVariableFont(font, {'wght': src['wght']})
        font.flavor = 'woff2'
        out = OUT_DIR / src['out']
        font.save(out)
        print(f"{key}: {out.relative_to(ROOT)} {out.stat().st_size / 1024:.0f} KB")
    GLYPH_LIST.write_text(text + '\n', encoding='utf-8')
    print(f'{len(text)} characters -> {GLYPH_LIST.relative_to(ROOT)}')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='*', help='extra files to scan (e.g. a scratch deck)')
    ap.add_argument('--check', action='store_true', help='only report characters missing from the subsets')
    ap.add_argument('--include-notes', action='store_true', help='also scan presenter notes')
    args = ap.parse_args()

    chars, _ = scan(args.files, args.include_notes)
    if args.check:
        return check(chars)
    build(chars)
    return 0


if __name__ == '__main__':
    sys.exit(main())

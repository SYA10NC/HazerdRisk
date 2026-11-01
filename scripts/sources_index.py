#!/usr/bin/env python3
"""research/ と news/ に載っているURLの索引を作る・照合する。

使い方:
  python3 scripts/sources_index.py            # research/SOURCES.md を再生成
  python3 scripts/sources_index.py --check URL [URL ...]
      # 既出URLなら「DUP <url> <ファイル>」、未出なら「NEW <url>」を出す
  python3 scripts/sources_index.py --dups     # 複数ファイルにまたがる既出URLを出す
"""
import collections, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL_RE = re.compile(r'https?://[^\s)\]>|`，、（）」]+')
TARGETS = ['research/[0-9][0-9]_*.md', 'news/[0-9][0-9][0-9][0-9]-[0-9][0-9].md']


def norm(u):
    u = u.rstrip('.。,;:').rstrip('/')
    u = re.sub(r'^http://', 'https://', u)
    u = re.sub(r'^https://www\.', 'https://', u)
    u = re.sub(r'https://(export\.|pdf\.)?arxiv\.org', 'https://arxiv.org', u)
    u = re.sub(r'arxiv\.org/(pdf|html)/', 'arxiv.org/abs/', u)
    u = re.sub(r'(arxiv\.org/abs/\d{4}\.\d{4,5})(v\d+)?(\.pdf)?', r'\1', u)
    return u


def build():
    idx = collections.defaultdict(set)
    for pat in TARGETS:
        for f in sorted(glob.glob(os.path.join(ROOT, pat))):
            rel = os.path.relpath(f, ROOT)
            for u in URL_RE.findall(open(f, encoding='utf-8').read()):
                idx[norm(u)].add(rel)
    return idx


def main():
    idx = build()
    args = sys.argv[1:]
    if args and args[0] == '--check':
        for u in args[1:]:
            n = norm(u)
            print(('DUP %s %s' % (u, ','.join(sorted(idx[n])))) if n in idx else 'NEW %s' % u)
        return
    if args and args[0] == '--dups':
        for u, fs in sorted(idx.items(), key=lambda x: (-len(x[1]), x[0])):
            if len(fs) > 1:
                print('%s\t%s' % (','.join(sorted(fs)), u))
        return
    out = ['# 既出ソース索引（自動生成）', '',
           '`python3 scripts/sources_index.py` で再生成する。手で編集しない。',
           '新しい調査では、ここにあるURLを「新規ソース」として数えない（再確認目的の再掲は可、その旨を注記）。', '',
           '- ユニークURL数: %d' % len(idx),
           '- 複数ファイルで重複: %d' % sum(1 for v in idx.values() if len(v) > 1), '']
    byfile = collections.defaultdict(list)
    for u, fs in idx.items():
        for f in fs:
            byfile[f].append(u)
    for f in sorted(byfile):
        out.append('## %s（%d件）' % (f, len(byfile[f])))
        out.append('')
        out += ['- %s' % u for u in sorted(byfile[f])]
        out.append('')
    open(os.path.join(ROOT, 'research/SOURCES.md'), 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote research/SOURCES.md (%d urls)' % len(idx))


if __name__ == '__main__':
    main()

#!/usr/bin/python3

from argparse import ArgumentParser
from pathlib import Path

import re

def write_qmds(base: Path, directory: Path, with_backup: bool = False):
    base_path = str(directory.relative_to(base))
    directory.mkdir()
    (directory / '_talk-inner.qmd').write_text('')
    if with_backup:
        (directory / '_talk-backup.qmd').write_text('')
    talk = f'---\nname: {directory.name}\n---\n'
    talk += '\n{{< include /' + base_path + '/_talk-inner.qmd >}}'
    if with_backup:
        talk += '\n# backup slides\n'
        talk += '\n{{< include /' + base_path + '/_talk-inner.qmd >}}'
    (directory / 'talk.qmd').write_text(talk)

def main():
    parser = ArgumentParser()
    parser.add_argument('target', type=Path)
    parser.add_argument('--base', type=Path, default=Path('.'))
    parser.add_argument('--with-backup', action='store_true', dest='backup')
    parser.add_argument('--without-backup', action='store_false', dest='backup')
    parser.set_defaults(backup=None)
    args = parser.parse_args()
    if args.backup == None:
        args.backup = (re.match(r'^\d+$', args.target.name) is None)
    write_qmds(base=args.base, directory=args.target, with_backup=args.backup)

if __name__ == '__main__':
    main()

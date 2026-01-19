#!/usr/bin/python3
import argparse
import logging
import shutil
import subprocess

from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

EXCLUDED = (
    'slides', 'talk', 'talk-handout', 'talk-handout-heldback', 'talk-slides', 'talk-slides-heldback', 'test',
    'talk-slides2',
)

def run_logged(command: List[str | Path]):
    logger.info('running %s', command)
    subprocess.check_call(command)

def convert_tex(base_file: Path, output_directory: Path, output_name: str = None):
    file_text = base_file.read_text()
    if r'\documentclass[tikz]{standalone}' in file_text[:500]:
        shutil.copyfile(base_file, output_directory / base_file.name)
    elif (base_file.stem.endswith('Tools') or base_file.stem.endswith('Lib')) \
        and '{frame' not in file_text and '{FragileFr' not in file_text:
        (output_directory / base_file.name).write_text(
            '<!--\n' +  file_text + '\n-->'
        )
    else:
        if output_name is None:
            output_name = ('_' + base_file.stem + '.qmd')
        run_logged([
            'python3', 'convert_lark.py',
            '--input', base_file,
            '--output', output_directory / output_name
        ])

def convert_directory(base_directory: Path, output_directory: Path):
    if not output_directory.exists():
        output_directory.mkdir()
    for item in base_directory.iterdir():
        if (item.suffix == '.pdf' or item.suffix == '.png' or item.suffix == '.jpg') and \
           item.stem not in EXCLUDED:
            shutil.copyfile(item, output_directory / item.name)
        elif item.is_dir() and item.name == 'figures':
            shutil.copytree(item, output_directory / item.name)
        elif item.suffix == '.tex' and \
           item.stem not in EXCLUDED:
           convert_tex(item, output_directory)

    if not (base_directory / 'talk-inner.tex').exists():
        convert_tex(base_directory / 'talk.tex', output_directory, '_talk-inner.qmd')
    run_logged([
        'python3', 'build.py',
        '--create-top-qmd', output_directory / 'talk.qmd',
        '--include', output_directory / '_talk-inner.qmd',
        '--backup-include', output_directory / '_talk-backup.qmd',
    ])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--new', action='store_true', default=False)
    parser.add_argument('directory', type=Path, nargs='+', default=[])
    args = parser.parse_args()
    for directory in args.directory:
        if args.new:
            inner_dir = directory / '_talk-inner.qmd',
            run_logged([
                'python3', 'build.py',
                '--create-top-qmd', directory / 'talk.qmd',
                '--empty',
            ])
        else:
            convert_directory(directory, Path.cwd() / directory.name)


#!/usr/bin/python3
import argparse
import copy
import logging
import os
import re
import subprocess

from pathlib import Path

USE_LATEXMK = True

LATEXRUN = [
    'latexrun', '--debug', '--verbose-cmds', '--latex-cmd', 'lualatex',
]

LATEXMK = [
    Path(__file__).parent / 'latexmk.pl', '-pdflua', '-outdir=latex.out',
]

QUARTO = [
    'quarto', 'render'
]

DECKTAPE = [
    'npx', 'decktape', 'reveal', '--fragments', '-s 1920x1080',
]


def run_logged(*args, **xargs):
    logging.debug('running %s', args)
    subprocess.check_call(*args, **xargs)

def build_figures(base_directory, incremental):
    env = copy.copy(os.environ)
    tex_inputs = []
    if env.get('TEXINPUTS'):
        tex_inputs = env.get('TEXINPUTS').split(':')
    tex_inputs.append(str(base_directory.absolute()))
    tex_inputs.append(str(Path('common').absolute()))
    tex_inputs.append(str(Path('.').absolute()))
    env['TEXINPUTS'] = ':'.join(tex_inputs) + ':'
    if not base_directory.exists():
        return
    for item in base_directory.iterdir():
        if item.name.endswith('.figure.tex'):
            fls_file = base_directory / 'latex.out' / item.with_suffix('.fls').name
            pdf_file = base_directory / 'latex.out' / item.with_suffix('.pdf').name
            pdf_is_outdated = True
            if incremental and fls_file.exists() and pdf_file.exists():
                pdf_is_outdated = False
                for line in fls_file.read_text().split('\n'):
                    if line.startswith('INPUT '):
                        input_raw_path = line[len('INPUT '):]
                        if input_raw_path.startswith('/'):
                            input_path = Path(input_raw_path)
                        else:
                            input_path = base_directory / input_raw_path
                        if not input_path.exists():
                            logging.debug('building %s because %s does not exist',
                                pdf_file, input_path)
                            pdf_is_outdated = True
                            break
                        elif input_path.stat().st_mtime > pdf_file.stat().st_mtime:
                            logging.debug('building %s because %s is new (%s v %s)',
                                pdf_file, input_path,
                                input_path.stat().st_mtime,
                                pdf_file.stat().st_mtime)
                            pdf_is_outdated = True
                            break
            if pdf_is_outdated:
                if USE_LATEXMK:
                    run_logged(
                        LATEXMK + [item.stem],
                        env=env,
                        cwd=base_directory,
                    )
                else:
                    run_logged(
                        LATEXRUN + [item.stem, '-o', pdf_file.relative_to(base_directory)],
                        env=env,
                        cwd=base_directory,
                    )
                assert pdf_file.exists()
                pdf_file.touch(exist_ok=True)
            svg_is_outdated = True
            pdf_info = subprocess.check_output([
                'pdfinfo', pdf_file
            ])
            page_count_match = re.search(rb'Pages:\s+(?P<pages>\d+)', pdf_info)
            pages = 1
            if page_count_match is not None:
                pages = int(page_count_match.group('pages'))
            if pages == 1:
                svg_files = [(1, item.with_suffix('.svg'))]
            else:
                svg_files = []
                for i in range(1, pages + 1):
                    svg_files.append(
                        (i, item.with_stem(item.stem + '-' + str(i)).with_suffix('.svg'))
                    )
            for page, svg_file in svg_files:
                if incremental:
                    needs_update = False
                    if pdf_is_outdated:
                        needs_update = True
                    elif svg_file.exists() and svg_file.stat().st_mtime > pdf_file.stat().st_mtime:
                        needs_update = False
                else:
                    needs_update = True
                if needs_update:
                    run_logged(['pdf2svg', pdf_file, svg_file, str(page)])

def render_qmd(path):
    run_logged(QUARTO + [path])

def create_top_qmd(path, include_path):
    path.write_text(f'---\ntitle: "{path.parent.name}"\n' +
'''
format:
  revealjs:
    theme: [simple, ../custom.scss]
    slide-level: 3
    navigation-mode: linear
    scrollable: true
    chalkboard: true
    progress: false
    margin: 0.02
    width: 1050
    height: 600
---
''' + '{{< include ../' + str(include_path.relative_to(path.parent.parent)) + ' >}}\n')

def render_html(path):
    run_logged(DECKTAPE + [path, path.with_suffix('.pdf')])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-top-qmd', type=Path)
    parser.add_argument('--render-qmd', type=Path)
    parser.add_argument('--render-html', type=Path)
    parser.add_argument('--figures', type=Path)
    parser.add_argument('--include', type=Path)
    parser.add_argument('--directory', type=Path)
    parser.add_argument('--incremental', action='store_true', default=True)
    parser.add_argument('--force', action='store_false', dest='incremental')
    args = parser.parse_args()
    if args.directory:
        args.figures = args.directory / 'texfig'
        args.render_qmd = args.directory / 'talk.qmd'
        args.render_html = args.directory / 'talk.html'
    if args.create_top_qmd:
        create_top_qmd(args.create_top_qmd, args.include)
    if args.figures:
        build_figures(args.figures, incremental=args.incremental)
    if args.render_qmd:
        render_qmd(args.render_qmd)
    if args.render_html:
        render_html(args.render_html)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

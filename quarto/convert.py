#!/usr/bin/python3
import argparse
import logging
import re

from pathlib import Path

def prepare_tokens(lst):
    result = []
    for pattern, token_id in lst:
        logging.debug('compiling %s', pattern)
        result.append((re.compile(pattern, re.X), token_id))
    return result

TIKZ_INLINE = False

# TODO: table style compact
# TODO: scrollable?
# TODO: minipage -> columns
# TODO: separate frames instead of fragments
# TODO: detect whether picture is whole slide
    # PROBABLY INVOLVES some lookahead, or pre-parsing of slide?
BASE_TOKENS = [
    (r'\\usetikzlibrary\{(?P<list>[^}]+)\}', 'usetikzlibrary'),
    (r'\\begin\{itemize\}', 'begin-itemize'),
    (r'\\end\{itemize\}', 'end-itemize'),
    (r'\\item(?:<(?P<when>[^>]+)>)?', 'item'),
    (r'\\vspace\{(?P<amount>[^}]+)\}', 'vspace'),
    (r'\\hspace\{(?P<amount>[^}]+)\}', 'hspace'),
    (r'''
        \\begin\{lstlisting\}\s*(?P<options>\[[^]]+\])?\s*\n
        (?P<contents>(?s:.)*?)
        \\end\{lstlisting\}''', 'lstlisting'),
    (r'''
        \\begin\{Verbatim\}\s*(?P<options>\[[^]]+\])?\s*\n
        (?P<contents>(?s:.)*?)
        \\end\{Verbatim\}
     ''', 'verbatim'),
    (r'''
        \\begin\{(?P<type>frame)\}\s*(?P<when><[^>+]>)?\s*(?:\[(?P<options>[^]]+)\])?\s*
        (?:\{(?P<title>[^}]+)\})?\s*
    ''', 'begin-frame'),
    (r'''
        \\begin\{(?P<type>FragileFrame)}\s*
     ''', 'begin-frame'),
    (r'\\frametitle\{(?P<title>[^}]+)\}', 'frametitle'),
    (r'\\end\{frame\}', 'end-frame'),
    (r'\\end\{FragileFrame\}', 'end-frame'),
    (r'''\\begin\{tikzpicture\}
        (?P<contents>(?s:.)*?)
        \\end\{tikzpicture\}
      ''',
     'tikzpicture'),
    (r'''\\myalttext\{[%\s]+
            \\begin\{tikzpicture\}
            (?P<contents>(?s:.)*?)
            \\end\{tikzpicture\}[%\s]+
        \}\{[%\s]*(?P<alt>[^}%]+)[%\s]*\}
      ''',
     'tikzpicture'),
    (r'''
        \\myemph(?:<(?P<when>[^>]+)>)?\{
      ''', 'start_myemph'),
    (r'\\(?P<sub>(?:sub)*)section\{(?P<name>[^}]+)\}', 'section'),
    (r'\\input\{(?P<input>[^}]+)\}', 'input'),
    (r'%.*', 'comment'),
    (r'\\\\(?:\[[^]]+\])?', 'linebreak'),
    (r'~', 'nbsp'),
    (r'``', 'start_dquote'),
    (r"''", 'end_dquote'),
    (r'`', 'start_quote'),
    (r"'", 'end_quote'),
    (r'\\begin{visibleenv}<(?P<when>[^>]+)>', 'begin_visibleenv'),
    (r'\\end{visibleenv}', 'end_visibleenv'),
    (r'\\hrule', 'hrule'),
    (r'\\texttt\{', 'tt_open'),
    (r'{\\tt', 'tt_open'),
    (r'{\\small\\tt', 'tt_open'),
    (r'{\\small', 'small_open'),
    (r'\\textit\{', 'it_open'),
    (r'\\sout\{', 'sout_open'),
    (r'\\ldots', 'ldots'),
    (r'\\checkmark', 'checkmark'),
    (r'\\begin\{tabular\}\{(?P<spec>[^}]+)\}', 'begin_tabular'),
    (r'\\end\{tabular\}', 'end_tabular'),
    (r'&', 'next_cell'),
    (r'\\fontsize\{[\d.]+\}\{[\d.]+\}(?:\\selectfont)', 'fontsize'),
    (r'\\multicolumn\{(?P<count>\d+)\}\{[^}]+\}\{', 'begin_multicolumn'),
    (r'\\hline', 'hline'),
    (r'}', 'close'),
    (r'{', 'open'),
    (r'\\(?P<c>[%{}_])', 'char'),
    (r'\\(?P<command>\w+)', 'unknown_command'),
    (r'(?P<c>.)', 'char'),
    (r'\n\s*', 'newline'),
]

def setup():
    global TOKENS
    TOKENS = prepare_tokens(BASE_TOKENS)

class Converter():
    def __init__(self, input_file: Path, base_output_file: Path):
        self._input_file = input_file
        self._base_output_file = base_output_file
        self._text = input_file.read_text()
        self._current_output = open(self._base_output_file, 'w')
        self._itemize_depth = 0
        self._last_token = None
        self._pending_item_div = False
        self._pending_separator = ''
        self._tikzlibraries: set[str] = set()
        self._figure_count = 0
        self._pending_close: list[str] = []
        self._position_line = 1
        self._position_char = 1
        self._in_tabular = False
        self._in_frame = False

    def _advance_position(self,text):
        for c in text:
            if c == '\n':
                self._position_line += 1
                self._position_char = 0
            else:
                self._position_char += 1

    def _next_token(self):
        for expression, token_id in TOKENS:
            #logging.debug('checking for %s', token_id)
            m = expression.match(self._text)
            if m == None:
                continue
            result = m.groupdict()
            result['id'] = token_id
            self._advance_position(m.group())
            self._text = self._text[m.end():]
            return result
        return None

    def emit(self, text):
        if self._pending_separator != '':
            if re.match('^\s+$', text):
                return
            self._current_output.write(self._pending_separator)
            self._pending_separator = ''
        self._current_output.write(text)

    def process_one(self):
        token = self._next_token()
        logging.debug('*** TOKEN = %s ', token)
        if token == None:
            if self._text != '':
                self.emit(f'*** PARSE ERROR ***\n{self._text}')
            return False
        token_id = token['id']
        token_id = token_id.replace('-', '_')
        try:
            getattr(self, f'process_{token_id}')(token)
        except Exception as e:
            raise Exception(f'at {self._input_file}:' +
                            f'{self._position_line}:{self._position_char}')
        except AttributeError as e:
            raise Exception(f'at {self._input_file}:' +
                            f'{self._position_line}:{self._position_char}')
        self._last_token = token
        return True

    def emit_header(self):
        self.emit('''---
filter:
  - tikz
format:
  revealjs:
    theme: simple
    slide-level: 3
    smaller: true
---
''')
    def process(self):
        while self.process_one():
            pass

    def process_begin_itemize(self, token):
        self._itemize_depth += 1

    def process_end_itemize(self, token):
        if self._pending_item_div:
            self.emit('\n:::\n')
            self._pending_item_div = False
        self._itemize_depth -= 1

    def process_vspace(self, token):
        self.emit('\n\n')
    
    def process_hspace(self, token):
        self.emit('&nbsp;&nbsp;')

    def process_lstlisting(self, token):
        self.emit(f'```\n{token["contents"]}```')

    def process_verbatim(self, token):
        self.emit(f'```\n{token["contents"]}```')

    def process_item(self, token):
        if self._pending_item_div:
            self.emit('\n:::\n')
            self._pending_item_div = False
        if self._pending_separator.strip() == '':
            self._pending_separator = ''
        self.emit('\n\n' + ('   ' * (self._itemize_depth - 1)) + '* ')

    def process_newline(self, token):
        if self._pending_separator.strip() == '':
            self._pending_separator = ''
        self._pending_separator += '\n' + ('   ' * self._itemize_depth)

    def process_char(self, token):
        self.emit(token['c'])

    def process_start_myemph(self, token):
        if self._last_token['id'] == 'item':
            self._pending_item_div = True
            if token['when']:
                self.emit('::: {.fragment fragment-index='+token["when"]+' .highlight-current-red})\n')
            else:
                self.emit('::: {color=orange font-style=italic}')
            self._pending_close.append('\n:::\n')
        else:
            self.emit(f'[')
            if token['when']:
                self._pending_close.append(
                    ']{.fragment fragment-index=' + token["when"] + \
                    ' .highlight-current-red}'
                )
            else:
                self._pending_close.append(
                    ']{color=orange font-style=italic}'
                )

    def process_usetikzlibrary(self, token):
        self._tikzlibraries |= set(token['list'].split(','))

    def process_tikzpicture(self, token):
        max_slide_number = 1
        for m in re.finditer(r'<(?P<n1>\d+)?-?(?P<n2>\d+)?>', token['contents']):
            for key in ('n1', 'n2'):
                if m.group(key):
                    max_slide_number = max(max_slide_number, int(m.group(key)))
        fig_output_dir = self._base_output_file.parent / 'figures' 
        logging.debug('fig_output_dir = %s', fig_output_dir)
        self._figure_count += 1
        fig_output_inner = fig_output_dir / (
            self._base_output_file.stem + f'-{self._figure_count}.inner.tex'
        )
        fig_output_inner.parent.mkdir(parents=True, exist_ok=True)
        with fig_output_inner.open('w') as out_fh:
            out_fh.write(r'\begin{tikzpicture}')
            out_fh.write('\n')
            out_fh.write(token['contents'])
            out_fh.write(r'\end{tikzpicture}')
            out_fh.write('\n')
        if max_slide_number > 1:
            self.emit('\n<div class="r-stack my-full">\n')
        for slide_number in range(1,max_slide_number+1):
            fig_output_tex = fig_output_dir / (
                self._base_output_file.stem + f'-{self._figure_count}-{slide_number}.figure.tex'
            )
            fig_output_svg = fig_output_tex.with_suffix('.svg')
            output_svg_name = fig_output_svg.parent.name + '/' + fig_output_svg.name
            fig_output_tex.parent.mkdir(parents=True, exist_ok=True)
            with fig_output_tex.open('w') as out_fh:
                out_fh.write(r'''
    \documentclass[tikz]{standalone}
    \input{common/tikzBase}
    '''
                )
                out_fh.write('\\usetikzlibrary{' + (','.join(list(self._tikzlibraries))) + '}\n')
                out_fh.write('\\setSlide{' + str(slide_number) + '}\n')
                out_fh.write(r'''\begin{document}''')
                out_fh.write('\n')
                out_fh.write('\\input{' + 
                    fig_output_inner.parent.parent.name + '/' +
                    fig_output_inner.parent.name + '/' +
                    fig_output_inner.name +
                '}\n')
                out_fh.write(r'''\end{document}''')
                out_fh.write('\n')
            if max_slide_number == 1:
                self.emit(f'![]({output_svg_name})\n\n')
            else:
                self.emit(f'![]({output_svg_name})' + '{.r-stretch .fragment .fade-in-then-out fragment-index=' +
                    str(slide_number) + '}\n')
        if max_slide_number > 1:
            self.emit('</div>\n')

    def process_begin_frame(self, token):
        title = token.get('title')
        if title == None:
            title = ''
        self._pending_separator += f'\n\n### {title}\n'

    def process_frametitle(self, token):
        title = token.get('title')
        self._pending_separator = self._pending_separator.replace(
            '### ',
            f'### {title}'
        )

    def process_end_frame(self, token):
        pass

    def process_comment(self, token):
        pass

    def process_input(self, token):
        input_file = token['input']
        if not input_file.endswith('.tex'):
            input_file += '.tex'
        input_file = input_file.replace('.tex', '.qmd')
        input_file = Path(input_file)
        input_file = input_file.with_name(
            '_' + input_file.name
        )
        self.emit('{{< include ' + str(input_file) + ' >}}\n')

    def process_tt_open(self, token):
        self._pending_close.append('</code>')
        self.emit('<code>')
 
    def process_small_open(self, token):
        self._pending_close.append('</small>')
        self.emit('<small>')

    def process_sout_open(self, token):
        self._pending_close.append('~~')
        self.emit('~~')

    def process_it_open(self, token):
        self._pending_close.append('</it>')
        self.emit(f'<it>')
    
    def process_open(self, token):
        self._pending_close.append('}')
        self.emit('{')

    def process_close(self, token):
        self.emit(self._pending_close.pop())

    def process_linebreak(self, token):
        if self._in_tabular:
            self._pending_separator += '</td></tr><td>'
        else:
            self.emit('<br>')
    
    def process_nbsp(self, token):
        self.emit('&nbsp;')

    def process_section(self, token):
        if token.get('sub'):
            self.emit(f'\n## {token["name"]}\n')
        else:
            self.emit(f'\n# {token["name"]}\n')

    def process_start_dquote(self, token):
        self.emit('\N{left double quotation mark}')
    
    def process_end_dquote(self, token):
        self.emit('\N{right double quotation mark}')

    def process_start_quote(self, token):
        self.emit('\N{left single quotation mark}')
    
    def process_end_quote(self, token):
        self.emit('\N{right single quotation mark}')

    def process_ldots(self, token):
        self.emit('\N{horizontal ellipsis}')

    def process_checkmark(self, token):
        self.emit('\N{check mark}')

    def process_unknown_command(self, token):
        self.emit('\\\\' + token['command'])

    def process_begin_tabular(self, token):
        self._in_tabular = True
        self.emit('<table>\n<tr>')
        self._pending_separator += '<td>'

    def process_end_tabular(self, token):
        self._pending_separator = ''
        self._in_tabular = False
        self.emit('</td></tr></table>')

    def process_next_cell(self, token):
        self._pending_separator += '</td><td>'

    def process_begin_multicolumn(self, token):
        self._pending_separator = self._pending_separator.replace(
            '<td>', 
            '<td colspan="' + token['count'] + '">'
        )
        # FIXME: should use pending_separator on close
        self._pending_close.append('')

    def process_fontsize(self, token):
        pass

    def process_vspace(self, token):
        pass

    def process_begin_visibleenv(self, token):
        when = token['when']
        if when.endswith('-'):
            when = when[:-1]
            self.emit('\n<div class="fragment fade-in" data-fragment-index=' + when +' >\n')
        else:
            self.emit('\n<div class="fragment fade-in-and-out" data-fragment-index=' + when +' >\n')
    def process_end_visibleenv(self, token):
        self.emit('\n</div>\n')

    def process_hrule(self, token):
        self.emit('\n<hr/>\n')

    def process_hline(self, token):
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--header', action='store_true')
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    setup()
    converter = Converter(input_file=args.input, base_output_file=args.output)
    if args.header:
        converter.emit_header()
    converter.process()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

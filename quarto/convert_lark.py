from __future__ import annotations

import argparse
import copy
import lark
import logging
import re
import sys
import unicodedata


from dataclasses import dataclass, field, InitVar
from lark import Lark, ast_utils
from itertools import chain
from operator import attrgetter, methodcaller
from pathlib import Path
from typing import Dict, List

current_module = sys.modules[__name__]

GRAMMAR = \
r'''
start: document

document: any_empty_item* (frame any_empty_item*)*

frame: _BEGIN_FRAME when? optional_argument? argument? whitespace? frametitle? any_text _END_FRAME
     |  _IFNOTHELDBACK document _END_BRACE -> heldback_frames
     |  _BRACE document _END_BRACE -> scoped_document
     |  _BEGIN_DOCUMENT document _END_DOCUMENT -> scoped_document

optional_argument: _SQUARE_BRACKET any_text _END_SQUARE_BRACKET

?argument: _BRACE any_text _END_BRACE

when: WHEN?

generic_command: SIMPLE_COMMAND when optional_argument? (_BRACE any_text _END_BRACE | _SQUARE_BRACKET any_text _END_SQUARE_BRACKET)*

?inline_command: generic_command
    | _BRACE any_text_raw any_text _END_BRACE -> bare_block
    | _BRACE SIMPLE_COMMAND+ any_text _END_BRACE -> block_with_command

item: _ITEM when any_text
    | _ITEM when whitespace? _BRACE _END_BRACE any_text
    | _ITEM when whitespace? _BRACE any_text _END_BRACE whitespace?

itemize: _BEGIN_ITEMIZE whitespace? SIMPLE_COMMAND? (whitespace? item)+ _END_ITEMIZE

tabular_line: (any_text_not_linebreak _NEXT_CELL)* any_text_not_linebreak LINEBREAK

tabular_line_nonl: (any_text_not_linebreak _NEXT_CELL)* any_text_not_linebreak 

tabular: _BEGIN_TABULAR _BRACE any_text_not_linebreak _END_BRACE tabular_line+ tabular_line_nonl whitespace? _END_TABULAR
       | _BEGIN_TABULAR _BRACE any_text_not_linebreak _END_BRACE tabular_line_nonl _END_TABULAR

frametitle: _BEGIN_FRAMETITLE _BRACE any_text _END_BRACE

?any_text: any_text LINEBREAK any_text
        | any_text_not_linebreak


any_text_not_linebreak: any_text_basic*
    | any_text_basic* inline_command generic_command* any_text_basic any_text_not_linebreak
    | any_text_basic* inline_command generic_command*

fontsize: _FONTSIZE _BRACE any_text _END_BRACE _BRACE any_text _END_BRACE -> fontsize

fontsize_group: _BRACE fontsize any_text _END_BRACE

?any_text_basic: _START_QUOTE any_text _END_QUOTE -> squote
    | _START_DQUOTE any_text _END_DQUOTE -> dquote
    | BEGIN_GENERIC any_text END_GENERIC -> generic_environment
    | itemize
    | tabular
    | fontsize
    | fontsize_group
    | whitespace
    | columns
    | VERBATIM -> verbatim
    | INLINE_VERBATIM -> inline_verbatim
    | TIKZPICTURE -> tikzpicture
    | _MYALTTEXT _BRACE whitespace? TIKZPICTURE whitespace? _END_BRACE _BRACE any_text _END_BRACE -> tikzpicture_with_alt
    | _MYALTTEXTB _BRACE whitespace? TIKZPICTURE whitespace? _END_BRACE _BRACE any_text _END_BRACE _BRACE any_text _END_BRACE -> tikzpicture_with_alt
    | _MYALTTEXTC _BRACE whitespace? TIKZPICTURE whitespace? _END_BRACE _BRACE any_text _END_BRACE _BRACE any_text _END_BRACE _BRACE any_text _END_BRACE -> tikzpicture_with_alt
    | _MYALTTEXTD _BRACE whitespace? TIKZPICTURE whitespace? _END_BRACE _BRACE any_text _END_BRACE _BRACE any_text _END_BRACE _BRACE any_text _END_BRACE _BRACE any_text _END_BRACE -> tikzpicture_with_alt
    | _PDFTOOLTIP _BRACE whitespace? TIKZPICTURE whitespace? _END_BRACE _BRACE any_text _END_BRACE -> tikzpicture_with_alt
    | _BEGIN_VISIBLEENV when any_text _END_VISIBLEENV -> visibleenv
    | _BEGIN_ONLYENV when any_text _END_ONLYENV -> visibleenv
    | _END_SQUARE_BRACKET -> end_square_bracket
    | _SQUARE_BRACKET -> square_bracket
    | LSTSET -> lstset
    | LSTINPUTLISTING -> lstinputlisting
    | TIKZSET -> tikz_context
    | NEWCOMMAND -> tikz_context
    | LRBOX -> tikz_context_begin_document
    | INCLUDE_GRAPHICS -> include_graphics
    | any_text_raw

columns: (column whitespace?)+

column: _BEGIN_MINIPAGE _BRACE any_text _END_BRACE any_text _END_MINIPAGE

whitespace: whitespace_item+
?whitespace_item: NEWLINE | WHITESPACE | COMMENT

?any_text_raw: ANY
    | NBSP | SIMPLE_ESCAPED
    | TIKZPICTURE | VERBATIM
    | DISPLAYMATH
    | INLINEMATH
    | UMLAT

any_empty_item: whitespace
    | SIMPLE_COMMAND when (_BRACE any_text _END_BRACE | _SQUARE_BRACKET any_text _END_SQUARE_BRACKET)* -> outside_command
    | BEGIN_GENERIC any_text END_GENERIC -> outside_environment
    | TIKZSET -> tikz_context
    | LSTSET -> lstset
    | NEWSAVEBOX -> tikz_context
    | NEWCOMMAND -> tikz_context
    | LRBOX -> tikz_context_begin_document
    | SAVEBOX -> tikz_context


COMMENT.5: /
        %.*|
        \\begin\{comment\}(?s:.*?)\n\s*\\end\{comment\}
    /x
_IFNOTHELDBACK.10: /\\iftoggle\{heldback\}\{\}\{/
_BEGIN_FRAMETITLE.10: /\\frametitle/
_BEGIN_ITEMIZE.10: /\\begin\{itemize\}/
_END_ITEMIZE.10: /\\end\{itemize\}/
_ITEM.10: /\\item/
_FONTSIZE.10: /\\fontsize/
WHEN: /<[^>]+>/
VERBATIM.10: /\\begin\{(?:Verbatim|lstlisting)\}\s*(?:\[[^]]+\])?
              \s*\n
              (?s:.*?)\n
              \\end\{(?:Verbatim|lstlisting)\}/x
INLINE_VERBATIM.10: /
        \\lstinline\|[^|]+\|
        |
        \\verb\*?\|[^|]+\|
        |
        \\lstinline![^!]+\!
        |
        \\verb\*?![^!]+\!
    /x
TIKZPICTURE.10: /\\begin\{tikzpicture\}\s*(?:\[[^]]+\])?\s*\n
                (?s:.*?)
                 \\end\{tikzpicture\}
                /x
_BEGIN_FRAME.10: /\\begin\{(?:frame|FragileFrame)\}/
_END_FRAME.10: /\\end{(?:frame|FragileFrame)\}/
_MYALTTEXT.10: /\\myalttext/
_MYALTTEXTB.10: /\\myalttextB/
_MYALTTEXTC.10: /\\myalttextC/
_MYALTTEXTD.10: /\\myalttextD/
_PDFTOOLTIP.10: /\\pdftooltip/
UMLAT.10: /\\\"./
DISPLAYMATH: /\\\[(?s:[^\]])*\\\]/
LINEBREAK: /\\\\(?:\[[^]]+\])?/
NBSP: /~/
_START_DQUOTE: /``/
_END_DQUOTE: /''/
_START_QUOTE: /`/
_END_QUOTE: /'/
_BEGIN_VISIBLEENV.10: /\\begin\{visibleenv\}/
_END_VISIBLEENV.10: /\\end\{visibleenv\}/
_BEGIN_ONLYENV.10: /\\begin\{onlyenv\}/
_END_ONLYENV.10: /\\end\{onlyenv\}/
_BEGIN_TABULAR.10: /\\begin\{tabular\}/
_END_TABULAR.10: /\\end\{tabular\}/
_BEGIN_MINIPAGE.10: /\\begin\{minipage\}/
_END_MINIPAGE.10: /\\end\{minipage\}/
_BEGIN_DOCUMENT.10: /\\begin\{document\}/
_END_DOCUMENT.10: /\\end\{document\}/
BEGIN_GENERIC.0: /\\begin\{(?!lrbox|comment|onlyenv|minipage|tabular|itemize|Verbatim|visibleenv|frame|FragileFrame|document)\w+\}/
END_GENERIC.0: /\\end\{(?!lrbox|comment|onlyenv|minipage|tabular|itemize|Verbatim|visibleenv|frame|FragileFrame|document)\w+\}/
_BRACE.-10: /\{/
_END_BRACE.-10: /\}/
_SQUARE_BRACKET: /\[/
_END_SQUARE_BRACKET: /\]/
INCLUDE_GRAPHICS.-10: /\\includegraphics\[[^]]+\]\{[^}]+\}/
SIMPLE_COMMAND.-10: /\\(?!begin|end|fontsize|_|lstset|tikzset|newsavebox|savebox|verb|lstinline|includegraphics)\w+\*?/
LSTINPUTLISTING.-10: /\\lstinputlisting
        (?:\[
            (?:
                [^{}]+
                |
                \{
                    (?:
                        \{
                            (?:
                                \{[^}]*\}
                            |
                                [^{}]+
                            )*
                        \}
                    |
                        [^{}]+
                    )*
                \}
            )*
        \])?\s*
        \{[^}]+\}
    /x
LSTSET.0: /\\lstset\{
        (?:
            [^{}]+
            |
            \{
                (?:
                    \{
                        (?:
                            \{[^}]*\}
                        |
                            [^{}]+
                        )*
                    \}
                |
                    [^{}]+
                )*
            \}
        )*
    \}/x
TIKZSET.0: /\\tikzset\{
        (?:
            [^{}]+
            |
            \{
                (?:
                    \{
                        (?:
                            \{
                                [^}]*
                            \}
                        |
                            [^{}]+
                        )*
                    \}
                |
                    [^{}]+
                )*
            \}
        )*
    \}/x
NEWSAVEBOX.0: /\\newsavebox\{\\[^}]+\}|\\newsavebox\\[a-zA-Z]+|\\ifdefined\\[a-zA-Z]+\\else\\newsavebox\\[a-zA-Z]+\\fi/
NEWCOMMAND.0: /\\(?:newcommand|renewcommand|providecommand)(?:<>)?\{[^}]+\}(?:
        \{(?:
            [^{}]+
            |
            \{
                (?:
                    \{
                        (?:
                            \{
                                [^}]*
                            \}
                        |
                            [^{}]+
                        )*
                    \}
                |
                    [^{}]+
                )*
            \}
        )*\}
        |
        \[[^\]]*\]
    )+
    /x
SAVEBOX.0: /
    \\savebox\{\\[^}]+\}\{
        (?:
            [^{}]+
            |
            \{
                (?:
                    \{
                        (?:
                            (?:
                                \{[^}]*\}
                            |
                                [^{}]+
                            )*
                        |
                            [^{}]+
                        )*
                    \}
                |
                    [^{}]+
                )*
            \}
        )*
    \}
    /x
LRBOX.0: /\\begin\{lrbox\}(?s:.*?)\\end\{lrbox\}/
INLINEMATH.-10: /\$[^$]+\$/
SIMPLE_ESCAPED.-11: /\\[.&_$%\/#{}]/
_NEXT_CELL.-20: /&/
NEWLINE.-20: /\n+/
WHITESPACE.-20: /[ \t\v]/
ANY.-30: /[^\\{}]/
'''

FIGURE_COUNT: Dict[str, int] = {}
SEEN_TIKZ_LIBRARIES: set[str] = set()

def _title_to_filename(title: str) -> str:
    result = title.replace(' ', '-')
    result = re.sub(r'[^-_a-zA-Z0-9]', '', result)
    if len(result) > 40:
        result = result[:40]
    return result

def _is_just_includegraphics(tikz_code: str) -> _SimpleFigure:
    m = re.match(r'''
        \s*
        \\begin\{tikzpicture\}(?:\[[^\]]+\])?
            \s*
            \\node\s*\[\s*(?:at=[^,=\]]+|anchor=[^,=\]]+)+\]\s*[^{]*\{\s*
                \\includegraphics(?:\[[^\]]+\])?\s*\{(?P<path>[^}]+)\}
            \s*\}\s*;\s*
        \\end\{tikzpicture\}
        \s*
    ''', tikz_code, re.X)
    if m is not None:
        return _SimpleFigure(m.group('path').replace('../', '/'))
    m = re.match(r'''
        \s*
        \\begin\{tikzpicture\}(?:\[[^\]]+\])?
            \s*
            \\node\s*\[(?P<options>[^\]]+)\]\s*
            \((?P<name>[^)]+)\)
            \s*
            at
            \s*
            \(current\s+page\.center\)
            \s*
            \{\s*
                \\includegraphics(?:\[[^\]]+\])?\s*\{(?P<path>[^}]+)\}
            \s*\}\s*;\s*
            \\node\s*\[[^\]]+\]\s*(?:\((?P<labelname>[^)]+)\)\s*)?
            at\s*\((?P<secondname>[^).]+)\.(?P<direction>[^)]+)\)
            \s*\{\s*
                (?P<label>[^}]+)
            \}\s*;\s*
        \\end\{tikzpicture\}
        \s*
    ''', tikz_code, re.X)
    if m is not None and m.group('name') == m.group('secondname') and 'label' not in m.group('options'):
        filename = m.group('path').replace('../', '/')
        label = m.group('label').replace('\\\\', ' ')
        return _SimpleFigure(filename, None, label)
    elif m is not None:
        assert False, m
    return None

@dataclass
class RenderContext:
    base_input_path: Path
    base_output_path: Path
    base_quarto_path: Path
    frame_count: int | None = None
    frame_title: str | None = None
    frame_label: str | None = None
    indent: int = 0
    strip_ends: bool = False
    column_count: int | None = None
    frame_top: bool = False
    pre: bool = False
    raw_html: bool = False
    tt: bool = False
    tikz_preamble: str = ''
    tikz_begin_document: str = ''
    lstset: List[str] = field(default_factory=lambda: [])
    nested_group: bool = False

    def next_figure_stem(self) -> str:
        global FIGURE_COUNT
        base_name = self.base_output_path.stem
        if base_name.startswith('_'):
            base_name = base_name[1:]
        if self.frame_count is None or self.frame_count > 1:
            if self.frame_label is not None:
                base_name = _title_to_filename(self.frame_label)
            elif self.frame_title is not None and self.frame_title != '':
                base_name += '-' + _title_to_filename(self.frame_title.lower())
        index = FIGURE_COUNT.get(base_name, 1)
        FIGURE_COUNT[base_name] = index + 1
        if index == 1:
            return f'{base_name}'
        else:
            return f'{base_name}_{index}'

    def get_tikz_libraries(self) -> set[str]:
        global SEEN_TIKZ_LIBRARIES
        return SEEN_TIKZ_LIBRARIES

    def add_tikz_libraries(self, libs: list[str]):
        global SEEN_TIKZ_LIBRARIES
        SEEN_TIKZ_LIBRARIES |= set(libs)

    def add_tikz_preamble(self, tikz_preamble: str):
        self.tikz_preamble += tikz_preamble

    def add_tikz_begin_document(self, tikz_begin_document: str):
        self.tikz_begin_document += tikz_begin_document

    def add_lstset(self, setting: str):
        self.lstset = self.lstset + [setting]

    def indented(self, markdown: str):
        return markdown.replace('\n', '\n' + (' ' * self.indent))

    def inner(self, strip_ends=None, extra_indent=None, column_count=None,
             frame_top=False, frame_title=None, frame_label=None,
             pre=None, tt=None, raw_html=None,
             nested_group=False) -> InnerRenderContextManager:
        result = copy.copy(self)
        if strip_ends is not None:
            result.strip_ends = strip_ends
        if extra_indent is not None:
            result.indent += extra_indent
        if column_count is not None:
            result.column_count = column_count
        if frame_top is not None:
            result.frame_top = frame_top
        if frame_title is not None:
            result.frame_title = frame_title
        if frame_label is not None:
            result.frame_label = frame_label
        if pre is not None:
            result.pre = pre
        if raw_html is not None:
            result.raw_html = raw_html
        if tt is not None:
            result.tt = tt
        if nested_group is not None:
            result.nested_group = nested_group
        return InnerRenderContextManager(result, self)

@dataclass
class InnerRenderContextManager:
    inner_context: RenderContext
    outer_context: RenderContext

    def __enter__(self):
        return self.inner_context
    
    def __exit__(self, typ, value, traceback):
        if not self.inner_context.nested_group:
            self.outer_context.tikz_preamble = self.inner_context.tikz_preamble
            self.outer_context.tikz_begin_document = self.inner_context.tikz_begin_document
            self.outer_context.lstset = self.inner_context.lstset
        return False
        

class _MyAstItem(ast_utils.Ast):
    @property
    def is_whitespace(self):
        return False

    @property
    def inner_text(self):
        raise Exception(f'no inner_text on {self}')

    @property
    def can_be_spanned(self) -> bool:
        return True

    """Approximate number of lines, primarily for purposes of guessing whether to mark a
    slide with .smaller."""
    @property
    def estimated_lines(self) -> float:
        return 0

    def render(self, context: RenderContext) -> str:
        return self.inner_text

@dataclass
class _RawString(_MyAstItem):
    contents: str
    contents_markdown: str | None = None

    @property
    def inner_text(self):
        return self.contents

    @property
    def estimated_lines(self) -> float:
        return len(self.contents) / 40

    def render(self, context: RenderContext) -> str:
        if self.contents_markdown:
            result = self.contents_markdown
        else:
            result = self.contents
        return context.indented(result)

@dataclass
class Lstset(_MyAstItem):
    token: lark.Token
    setting: str

    def __init__(self, token):
        self.token = token
        m = re.match(r'''\\lstset\{(?P<setting>
                (?:
                    [^{}]+
                    |
                    \{
                        (?:
                            \{[^}]*\}
                        |
                            [^{}]+
                        )*
                    \}
                )*
            )\}''', token.value, re.X)
        assert m is not None, token.value
        self.setting = m.group('setting')

    @property
    def inner_text(self):
        return ''

    def render(self, context: RenderContext) -> str:
        context.add_lstset(self.setting)
        return '<!-- ' + str(self.token) + ' -->\n'

@dataclass
class TikzContext(_MyAstItem):
    text: str

    def __init__(self, *args):
        self.text = ''
        for arg in args:
            self.text += str(arg)
        if self.text.startswith(r'\newcommand<>'):
            m = re.search(r'''
                    \\newcommand<>\{(?P<command>[^}]+)\}\[1\]
                ''', self.text, re.X)
            assert m is not None
            self.text = re.sub(r'''
                    \\newcommand<>\{(?P<command>[^}]+)\}\[1\]
                ''',
                r'\\NewDocumentCommand\g<command>{D<>{} m}',
                self.text, flags=re.X)
            logging.debug('self.text = %s', self.text)
        elif r'\newcommand<' in self.text:
            assert False

    @property
    def inner_text(self):
        return self.text

    def render(self, context: RenderContext) -> str:
        context.add_tikz_preamble(self.text + '\n')
        return ''

# For things like lrbox which seem broken if done in the preamble
@dataclass
class TikzContextBeginDocument(TikzContext):
    def render(self, context: RenderContext) -> str:
        context.add_tikz_begin_document(self.text + '\n')
        return ''

@dataclass
class TikzSavebox(TikzContext):
    def __init__(self, *args):
        self.text = ''
        for arg in args:
            if isinstance(arg, Whitespace):
                self.text += ''.join(map(str, arg.parts))
            else:
                self.text += str(arg)
        self.text += '}'

@dataclass
class OptionalArgument(_MyAstItem):
    contents: AnyText

    @property
    def inner_text(self) -> str:
        return self.contents.inner_text

    def render(self, context: RenderContext) -> str:
        return ''


@dataclass
class When(_MyAstItem):
    raw_when: InitVar[str | None] = None
    when: str | None = field(init=False)
    before_index: int | None = field(init=False)
    middle_indices: tuple[int] = field(init=False)
    after_index: int | None = field(init=False)


    def __post_init__(self, raw_when):
        if raw_when:
            self.when = raw_when[1:-1]
            self.when = self.when.replace('all:', '')
            when_parts = re.split(r'[,|]', self.when)
            self.before_index = None
            self.after_index = None
            middle_indices = []
            for part in when_parts:
                part = part.replace('all:','')
                if part.startswith('handout:'):
                    continue
                if part != '1-' and part.startswith('1-'):
                    part = part[1:]
                if part.startswith('-'):
                    if self.before_index is not None:
                        raise ValueError(f'multiple before ranges in {raw_when}')
                    self.before_index = int(part[1:])
                elif part.endswith('-'):
                    if self.after_index is not None:
                        raise ValueError(f'multiple after ranges in {raw_when}')
                    self.after_index = int(part[:-1])
                elif '-' in part:
                    before, after = part.split('-')
                    for i in range(int(before), int(after)+1):
                        middle_indices.append(i)
                else:
                    middle_indices.append(int(part))
            self.middle_indices = tuple(middle_indices)
        else:
            self.when = None
            self.before_index = None
            self.middle_indices = tuple()
            self.after_index = None
        if self.after_index == 1:
            self.when = None
            self.before_index = None
            self.middle_indices = tuple()
            self.after_index = None

    @property
    def needs_fragment(self):
        if self.when:
            return True
        else:
            return False
   
    @property 
    def is_after_fragment(self):
        return self.after_index is not None

    @property 
    def is_before_fragment(self):
        return self.before_index is not None

    @property
    def is_multiple(self):
        count = len(self.middle_indices)
        if self.after_index is not None:
            count += 1
        if self.before_index is not None:
            count += 1
        return count > 0

    @property
    def number(self) -> int:
        if self.is_multiple:
            raise ValueError
        if len(self.middle_indices) > 0:
            return self.middle_indices[0]
        elif self.after_index is not None:
            return self.after_index
        elif self.before_index is not None:
            return self.before_index
        else:
            return ValueError


@dataclass
class _InlineCommand(_MyAstItem):
    command: str
    arguments: List[AnyText]
    when: When | None = None

    @property
    def inner_text(self):
        if len(self.arguments) == 0:
            return self.command
        else:
            return ''.join(map(attrgetter('inner_text'), self.arguments)).strip()

    @property
    def can_be_spanned(self) -> bool:
        return all(map(attrgetter('can_be_spanned'), self.arguments))

    @property
    def estimated_lines(self) -> float:
        if self.command in (r'\vspace', r'\hrule'):
            return 1.5
        else:
            return sum(map(attrgetter('estimated_lines'), self.arguments))

    def render(self, context: RenderContext) -> str:
        before, after = None, None
        start_arg : int | None = -1
        is_tt = None
        strip_ends = None
        when = self.when
        command = self.command
        arguments = self.arguments
        if re.match(r'^\\myemph[A-Z]$', command) is not None:
            index = ord(command[len(r'\myemph')]) - ord('A')
            when = When(f'<{index}>')
            assert when.needs_fragment
            command = r'\myemph'
        if re.match(r'^\\myemph(AB|Two|Three|Four|Five|Six|Seven)$', command) is not None:
            name = command[len(r'\myemph'):]
            index = {
                'AB': '2-3',
                'Two': 2,
                'Three': 3,
                'Four': 4,
                'Five': 5,
                'Six': 6,
                'Seven': 7,
            }[name]
            when = When(f'<{index}>')
            assert when.needs_fragment
            command = r'\myemph'
        if command == r'\varMark':
            logging.debug('arguments = %s', arguments)
            index_argument = arguments[0].inner_text
            when = When(f'<{index_argument}>')
            command = r'\myemph'
            arguments = arguments[1:]
        if when and when.needs_fragment:
            if command in (r'\myemph',r'\btHL',):
                before = ''
                after = ''
                if when.is_after_fragment:
                    before += '['
                    after += ']{.fragment fragment-index=' + str(when.after_index) + ' .custom .myem}'
                if when.is_before_fragment:
                    before += '['
                    after += ']{.fragment fragment-index=' + str(when.before_index+1) + ' .custom .myem-until}'
                for index in when.middle_indices:
                    before += '['
                    after += ']{.fragment fragment-index=' + str(index) + ' .custom .myem-only}'
            else:
                when_str = ''
                if when.raw_when is not None:
                    when_str = str(when_raw_when)
                before, after = self.command + when_str + '{', '}'
        else:
            assert '<' not in command, command
            assert '&' not in command, command
            if command in (r'\tt', r'\texttt'):
                before, after = '<code>', '</code>'
                if len(arguments) > 0:
                    inner = arguments[0].get_interesting_parts()
                    if len(inner) == 1:
                        if isinstance(inner[0], _InlineCommand) and len(inner[0].arguments) > 0:
                            inner_inner = inner[0].arguments[-1].get_interesting_parts()
                            if len(inner_inner) == 1:
                                inner = inner_inner
                        if isinstance(inner[0], Tabular):
                            before, after = '', ''
                            is_tt = True
                    else:
                        logging.debug('inner = %s', inner)
                strip_ends = True
            elif command in (r'\myemph',r'\btHL',):
                before, after = '<em>', '</em>'
            elif command in (r'\textit', r'\itshape', r'\it'):
                before, after = '<i>', '</i>'
            elif command in (r'\textbf', r'\bfseries'):
                before, after = '<em>', '</em>'
            elif command in (r'\small',r'\scriptsize'):
                can_be_spanned = all(map(attrgetter('can_be_spanned'), arguments))
                if can_be_spanned:
                    before, after = '[', ']{.my-small}'
                else:
                    before, after = '<div class="my-small">', '</div>\n'
            elif command in (r'\selectfont',):
                before, after = '', ''
            elif command in (r'\hspace',):
                start_arg = None
                before, after = ' ', ''
            elif command in (r'\hrule',):
                start_arg = None
                before, after = '<hr />', '\n'
            elif command in (r'\vspace',):
                start_arg = None
                if arguments[0].inner_text.startswith('-'):
                    before, after = '\n', ''
                else:
                    before, after = '\n<hr class="vspace" />', ''
            elif command in (r'\textasciicircum',):
                before, after = '^', ''
            elif command in (r'\ldots,'):
                before, after = '\N{horizontal ellipsis}', ''
            elif command in (r'\sout',):
                before, after = '~~', '~~'
            elif command in (r'\imagecredit',):
                before, after = '[', ']{.mycredit}'
            elif command in (r'\url',):
                before, after = '[', '](' + arguments[0].inner_text + ')'
            elif command in (r'\titlepage',):
                return ''
            elif command in (r'\normalfont',):
                before, after = '<span class="normal">', ''
            elif command in (r'\textcolor',r'\color'):
                color_map = {
                    'violet!80!black': 'darkviolet',
                    'blue!80!black': 'darkblue',
                    'green!80!black': 'darkgreen',
                }
                color = color_map.get(arguments[0].inner_text, arguments[0].inner_text)
                before, after = f'<span style="color: {color}">', '</span>'
            else:
                start_arg = 0
                before, after = command.replace('\\', '\\\\') + '{', '}'

        if context.raw_html and before == '[':
            classes = []
            attrs = {}
            for span_class in re.findall(r'\.[\w-]+|[\w-]+=\w+', after):
                if '=' in span_class:
                    k, v = span_class.split('=')
                    attrs['data-' + k] = v
                else:
                    classes.append(span_class[1:])
            if len(classes) > 0:
                attrs['class'] = " ".join(classes)
            before = '<span '
            for k, v in attrs.items():
                before += f'{k}="{v}" '
            before = before[:-1]
            before += '>'
            after = '</span>'
        result = before
        if start_arg != None:
            for argument in arguments[start_arg:]:
                with context.inner(tt=is_tt, strip_ends=strip_ends, frame_top=None) as inner_context:
                    result += argument.render(inner_context)
        result += after
        return result

@dataclass
class Lstinputlisting(_MyAstItem):
    raw_input: InitVar[str | None] = None
    file_name: str = field(init=False)
    options: str | None = field(init=False)

    def __post_init__(self, raw_input):
        m = re.match(r'''\\lstinputlisting
                (?:\[(?P<options>
                    (?:
                        [^{}]+
                        |
                        \{
                            (?:
                                \{
                                    (?:
                                        \{[^}]*\}
                                    |
                                        [^{}]+
                                    )*
                                \}
                            |
                                [^{}]+
                            )*
                        \}
                    )*
                )\])?\s*
                \{(?P<filename>[^}]+)\}
            ''', str(raw_input), re.X)
        assert m is not None, raw_input
        self.options = m.group('options')
        self.filename = m.group('filename')

    @property
    def estimated_lines(self) -> int:
        return 8

    def render(self, context: RenderContext) -> str:
        file_path = context.base_input_path.parent / self.file_name
        output_path = (context.base_output_path.parent / file_path.name)
        output_path.write_text(file_path.read_text())
        result = ''
        if self.options is not None:
            result += f'\n<!-- lsting options: {self.options} -->'
        result += '\n```\n{{< include /' + str(
            output_path.relative_to(context.base_quarto_path)) + ' >}}\n```\n'

@dataclass
class Fontsize(_MyAstItem):
    def __init__(self, *args):
        pass

    def render(self, context: RenderContext) -> str:
        return ''

def _merge_rawstrings(lst):
    pending = None
    result = []
    for item in lst:
        if pending is None and isinstance(item, _RawString):
            pending = item
        elif pending is not None:
            if isinstance(item, _RawString):
                pending_markdown = pending.contents_markdown
                if pending_markdown is None:
                    pending_markdown = pending.contents
                item_markdown = item.contents_markdown
                if item_markdown is None:
                    item_markdown = item.contents
                pending = _RawString(
                    pending.contents + item.contents,
                    pending_markdown + item_markdown
                )
            else:
                result.append(pending)
                pending = None
                result.append(item)
        else:
            result.append(item)
    if pending is not None:
        result.append(pending)
    return result

@dataclass
class AnyText(_MyAstItem):
    parts: List[_MyAstItem]

    def __init__(self, *parts):
        self.parts = []
        for part in parts:
            if isinstance(part, AnyText):
                self.parts += part.parts
            else:
                self.parts.append(part)
        self.parts = _merge_rawstrings(self.parts)

    @property
    def is_whitespace(self):
        return self.inner_text.strip() == ''

    @property
    def can_be_spanned(self) -> bool:
        return all(map(attrgetter('can_be_spanned'), self.parts))

    @property
    def inner_text(self) -> str:
        return ''.join(map(attrgetter('inner_text'), self.parts))

    @property
    def estimated_lines(self) -> float:
        return sum(map(attrgetter('estimated_lines'), self.parts))

    def get_interesting_parts(self) -> List[_MyAstItem]:
        result = []
        for part in self.parts:
            if isinstance(part, _RawString) or isinstance(part, Whitespace):
                continue
            result.append(part)
        return result

    def render(self, context: RenderContext) -> str:
        start = 0
        end = len(self.parts) - 1
        if context.strip_ends:
            start = 0
            while start < len(self.parts) and self.parts[start].is_whitespace:
                start += 1
            end = len(self.parts) - 1
            while end >= 0 and self.parts[end].is_whitespace:
                end -= 1
        for item in self.parts[start:end+1]:
            if isinstance(item, lark.Tree):
                logging.debug('found tree %s', item)
        if end == start:
            return self.parts[start].render(context)
        else:
            with context.inner(strip_ends=False) as inner_context:
                result = ''.join(map(
                    methodcaller('render', inner_context),
                    self.parts[start:end+1]
                ))
                return result

AnyTextNotLinebreak = AnyText
AnyTextNotAfterCommand = AnyText

@dataclass
class FontsizeGroup(_MyAstItem):
    fontsize: Fontsize
    text: AnyText

    def render(self, context: RenderContext) -> str:
        return self.text.render(context)

    @property
    def estimated_lines(self) -> float:
        return self.text.estimated_lines

    @property
    def inner_text(self) -> str:
        return self.text.inner_text


@dataclass
class Column(_MyAstItem):
    width: AnyText
    contents: AnyText

    def render(self, context: RenderContext) -> result:
        width_text = self.width.inner_text
        if r'\textwidth' in width_text:
            width_float = float(width_text.replace(r'\textwidth', ''))
        else:
            width_float = 1.0 / context.column_count
        result = '\n::: {.column width="' + f'{width_float * 99.0:.0f}%' + '"}\n'
        with context.inner() as inner_context:
            result += self.contents.render(inner_context)
        result += '\n:::\n'
        return result

    @property
    def estimated_lines(self) -> float:
        return self.contents.estimated_lines

@dataclass
class Columns(_MyAstItem):
    columns: List[Column]

    def __init__(self, *items):
        columns = []
        for item in items:
            if not item.is_whitespace:
                columns.append(item)
        self.columns = columns

    @property
    def estimated_lines(self) -> float:
        return max(map(attrgetter('estimated_lines'), self.columns))

    def render(self, context: RenderContext) -> str:
        with context.inner(column_count=len(self.columns)) as inner_context:
            result = '\n:::: {.columns}\n'
            for column in self.columns:
                result += column.render(inner_context)
            result += '\n::::\n'
            return result


@dataclass
class Moredelim:
    start: str
    end: str
    command: str

    def generate_command(self, current_argument: str) -> GenericCommand | AnyText:
        current_inner = AnyText(_RawString(current_argument))
        for command in reversed(self.command.split('\\')):
            if command == '':
                continue
            m = re.match(r'(?P<base_command>[^{<]+)(?:(?P<when><[^>]+>))?(?:\{(?P<arg>[^}]+)\})?',
                command)
            assert m is not None, command
            when = None
            if m.group('when') is not None:
                when = When(m.group('when'))
            args: list[AnyText] = []
            if m.group('arg'):
                args.append(AnyText(_RawString(m.group('arg'))))
            args.append(current_inner)
            logging.debug('verbatim command %s/%s from %s', m.group('base_command'), when, command)
            assert not m.group('base_command').startswith('\\'), self.command
            current_inner = AnyText(
                GenericCommand(
                    '\\' + m.group('base_command'),
                    when,
                    *args
                )
            )
        return current_inner

def _parse_moredelim_from(settings):
    result = []
    for m in re.finditer(r'''
        moredelim=\{?[^]]+\[[^]]+\] # {**[is]
            \[(?P<command>[^]]+)\] # [\it]
            \{(?P<start>[^}]+)\} # {X}
            \{(?P<end>[^}]+)\} # {Y}
        ''', settings, re.X):
        result.append(Moredelim(
            m.group('start'),
            m.group('end'),
            m.group('command'),
        ))
    return result

@dataclass
class InlineVerbatim(_MyAstItem):
    contents: str

    def __init__(self, token):
        value = token.value
        for prefix in (r'\lstinline', r'\verb*', r'\verb'):
            if value.startswith(prefix):
                value = value[len(prefix):]
                break 
        self.contents = value[1:-1]

    @property
    def inner_text(self):
        return self.contents

    def render(self, context: RenderContext) -> str:
        return f'`{self.contents}`'


@dataclass
class Verbatim(_MyAstItem):
    contents: str
    command_chars: str | None = None
    moredelim: list[(str, str, str)] | None = None

    @property
    def estimated_lines(self) -> float:
        return self.contents.count('\n')

    def __init__(self, token):
        pattern = r'''
              \\begin\{(?:Verbatim|lstlisting)\}\s*(?:\[
                (?:
                    [^\[\]]+
                    |
                    \[[^\]]*\]
                )+
              \])?
              \s*\n(?P<contents>(?s:.)*?)
              \\end\{(?:Verbatim|lstlisting)\}
        '''
        logging.debug('about to match %s', token.value)
        m = re.match(pattern, token.value, re.X)
        assert m is not None, token.value
        self.contents = m.group('contents')
        m = re.search(r'commandchars=([^]]+)', token.value)
        if m != None:
            self.command_chars = m.group(1)
            self.command_chars = re.sub(r'\\(.)', r'\1', self.command_chars)
        self.moredelim = _parse_moredelim_from(token.value)

    @property
    def can_be_spanned(self) -> bool:
        return False

    def render(self, context: RenderContext) -> str:
        active_moredelim = self.moredelim + list(chain.from_iterable(
            map(_parse_moredelim_from, context.lstset)
        ))
        logging.debug('active_moredelim = %s from %s, %s',
            active_moredelim, self.moredelim, context.lstset)
        if self.command_chars is not None or len(active_moredelim) > 0:
            if self.command_chars is None:
                slash = None
                open_brace = None
                close_brace  = None
            else:
                slash = self.command_chars[0]
                open_brace = self.command_chars[1]
                close_brace = self.command_chars[2]
            logging.debug('\\/{/} = %s/%s/%s', slash, open_brace, close_brace)
            result = '\n<pre><code>'
            in_command = False
            in_argument = False
            current_moredelim: Moredelim | None = None
            current_command = ''
            previous_arguments = []
            current_argument = ''
            i = 0
            while i < len(self.contents):
                c = self.contents[i]
                if current_moredelim is not None and self.contents[i:].startswith(current_moredelim.end):
                    current_inner = current_moredelim.generate_command(current_argument)
                    logging.debug('got command %s', current_inner)
                    with context.inner(pre=True, raw_html=True) as inner_context:
                        result += current_inner.render(inner_context)
                    i += len(current_moredelim.end)
                    current_argument = ''
                    current_moredelim = None
                    continue
                elif in_argument or current_moredelim is not None:
                    if in_argument and c == close_brace:
                        previous_arguments.append(_RawString(current_argument))
                        current_argument = ''
                        if len(self.contents) < i+1 or self.contents[i+1] != open_brace:
                            assert not current_command.startswith('\\'), current_command
                            command_ast = GenericCommand(
                                    '\\' + current_command,
                                    None,
                                    *previous_arguments
                                )
                            with context.inner(pre=True, raw_html=True) as inner_context:
                                result += command_ast.render(inner_context)
                            in_argument = False
                            current_command = ''
                            previous_arguments = []
                        else:
                            i += 2
                            continue
                    elif c == '<':
                        current_argument += '&lt;'
                    elif c == '>':
                        current_argument += '&gt;'
                    elif c == '&':
                        current_argument += '&amp;'
                    elif c == '\n':
                        current_argument += '\n'
                    else:
                        current_argument += c
                elif in_command:
                    if c == open_brace:
                        in_command = False
                        in_argument = True
                        logging.debug('finished command name %s', current_command)
                        current_argument = ''
                    else:
                        current_command += c
                else:
                    for candidate in active_moredelim:
                        if self.contents[i:].startswith(candidate.start):
                            i += len(candidate.start)
                            current_moredelim = candidate
                            break
                    if current_moredelim is not None:
                        continue
                    if c == slash:
                        logging.debug('found command at %s', self.contents[i:i+10])
                        in_command = True
                    elif c in '[\\':
                        result += '\\' + c
                    elif c == '<':
                        result += '&lt;'
                    elif c == '>':
                        result += '&gt;'
                    elif c == '&':
                        result += '&amp;'
                    elif c == '\n':
                        result += '\n'
                    else:
                        result += c
                i += 1
            result += '</code></pre>\n'
            return result
        else:
            return f'\n```\n{self.contents}\n```\n'

@dataclass
class Visibleenv(_MyAstItem):
    when: When
    contents: AnyText

    @property
    def estimated_lines(self) -> float:
        return self.contents.estimated_lines

    @property
    def can_be_spanned(self) -> bool:
        return False

    def render(self, context: RenderContext) -> str:
        when = self.when
        if when.needs_fragment:
            if when.is_multiple:
                raise NotImplemented
            elif when.is_after_fragment:
                number = str(when.after_index)
                result = context.indented(
                    '\n<div class="fragment fade-in" data-fragment-index=' + number + ' >\n'
                )
            elif when.is_before_fragment:
                number_plus_1 = str(when.before_index + 1)
                result = context.indented(
                    '\n<div class="fragment fade-out" data-fragment-index=' + number_plus_1 + ' >\n')
            else:
                number = str(when.middle_indices[0])
                result = context.indented(
                    '\n<div class="fragment fade-in-and out" data-fragment-index=' + number +' >\n'
                )
            result += self.contents.render(context)
            result += '\n</div>'
            return result
        else:
            return self.contents.render(context)

def _make_fig_alt(alt_text: str | None) -> str:
    if alt_text is None:
        return ''
    else:
        alt_text_escaped = alt_text.replace('"', '&quot;')
        alt_text_escaped = alt_text_escaped.replace('\n', ' ')
        alt_text_escaped = alt_text_escaped.strip()
        maybe_alt = f' fig-alt="{alt_text_escaped}"'
        return maybe_alt

@dataclass
class _SimpleFigure(_MyAstItem):
    filename: str
    alt_text: str | None = None
    caption: str = ''

    @property
    def estimated_lines(self) -> float:
        return 4

    def render(self, context: RenderContext) -> str:
        maybe_alt = _make_fig_alt(self.alt_text)
        return f'\n![{self.caption}]({self.filename})' + '{' + maybe_alt + '}\n'

@dataclass
class IncludeGraphics(_SimpleFigure):
    def __init__(self, token):
        m = re.match(r'''
            \\includegraphics\[(?P<options>[^]]+)\]
                \{
                    (?P<filename>[^}]+)
                \}
        ''', token.value, re.X)
        assert m is not None, token.value
        self.filename = m.group('filename')
        self.filename = self.filename.replace('../', '/')

@dataclass
class Tikzpicture(_MyAstItem):
    contents: lark.Token
    alt_texts: list[str] | None = None

    @property
    def estimated_lines(self) -> float:
        return 4

    @property
    def can_be_spanned(self) -> bool:
        return False

    def render(self, context: RenderContext) -> str:
        real_figure = _is_just_includegraphics(self.contents.value)
        if real_figure is not None:
            return real_figure.render(context)
        max_slide_number = 1
        for m in re.finditer(r'<(?P<n1>\d+)?-?(?P<n2>\d+)?>', self.contents.value):
            for key in ('n1', 'n2'):
                if m.group(key):
                    max_slide_number = max(max_slide_number, int(m.group(key)))
        tikz_code = self.contents.value
        if 'pic cs:' in tikz_code:
            return '<!--\n```\n' + self.contents.value + '\n```\n-->\n'
        tikz_code = tikz_code.replace(r'\paperwidth', r'\mypaperwidth')
        tikz_code = tikz_code.replace(r'\paperheight', r'\mypaperheight')
        tikz_code = tikz_code.replace(r'\textwidth', r'\mypaperwidth')
        tikz_code = tikz_code.replace(r'\textheight', r'\mypaperheight')
        options_match = re.search(r'\\begin\{tikzpicture\}\[(?P<options>[^]]+)\]', tikz_code)
        is_overlay = False
        if options_match is not None:
            if 'overlay' in options_match.group('options'):
                is_overlay = True
                logging.debug('options = %s', options_match.group('options'))
                assert r'\begin{tikzpicture}[' in tikz_code
                assert r'\begin{tikzpicture}[' + options_match.group('options') in tikz_code
                tikz_code = tikz_code.replace(
                    r'\begin{tikzpicture}[' + options_match.group('options') + ']',
                    r'\begin{tikzpicture}' + '\n'
                    r'\node[minimum width=15cm,minimum height=9cm] (current page) {};' + '\n'
                    r'\begin{scope}[overlay]' + '\n'
                )
                tikz_code = tikz_code.replace(
                    r'\end{tikzpicture}',
                    r'\end{scope}' + '\n'
                    r'\end{tikzpicture}' + '\n'
                )
        fig_output_dir = context.base_output_path.parent / 'texfig' 
        fig_file_stem = context.next_figure_stem()
        fig_output_inner = fig_output_dir / (
            fig_file_stem + '.inner.tex'
        )
        fig_output_inner.parent.mkdir(parents=True, exist_ok=True)
        with fig_output_inner.open('w') as out_fh:
            out_fh.write(tikz_code)
        result = ''
        if not is_overlay:
            if max_slide_number > 1:
                if context.frame_top:
                    result += '\n\n::: {.r-stack .my-full}\n'
                else:
                    result += '\n\n::: {.r-stack}\n'
        fig_output_tex = fig_output_dir / (
            fig_file_stem + f'.figure.tex'
        )
        fig_output_tex.parent.mkdir(parents=True, exist_ok=True)
        with fig_output_tex.open('w') as out_fh:
            out_fh.write(r'\documentclass[tikz]{standalone}' + '\n')
            out_fh.write(r'\input{common/tikzBase}' + '\n')
            out_fh.write('\\usetikzlibrary{' + (','.join(list(context.get_tikz_libraries()))) + '}\n')
            out_fh.write(context.tikz_preamble)
            out_fh.write(r'''\begin{document}''' + '\n')
            out_fh.write(context.tikz_begin_document)
            out_fh.write('\n')
            for slide_number in range(1, max_slide_number+1):
                out_fh.write('\\setSlide{' + str(slide_number) + '}\n')
                out_fh.write('\\input{' + 
                    fig_output_inner.parent.parent.name + '/' +
                    fig_output_inner.parent.name + '/' +
                    fig_output_inner.name +
                '}\n')
            out_fh.write(r'''\end{document}''')
            out_fh.write('\n')
        for slide_number in range(1, max_slide_number+1):
            if max_slide_number == 1:
                fig_output_svg = fig_output_tex.with_suffix('.svg')
            else:
                fig_output_svg = fig_output_tex.with_stem(
                    fig_output_tex.stem + f'-{slide_number}'
                ).with_suffix('.svg')
            output_svg_name = '/' + str(fig_output_svg.relative_to(context.base_quarto_path))
            maybe_alt = ''
            if self.alt_texts is not None:
                if slide_number > len(self.alt_texts):
                    alt_text = self.alt_texts[-1]
                else:
                    alt_text = self.alt_texts[slide_number-1]
                maybe_alt = _make_fig_alt(alt_text)
            if is_overlay:
                result += f'![]({output_svg_name})' + \
                    '{.absolute top="0%" left="0%" width=1050 height=600 .my-center ' + maybe_alt
                if max_slide_number > 1:
                    result += ' .fragment .fade-in-then-out fragment-index='+str(slide_number)
                result += '}\n'
            elif max_slide_number == 1:
                result += f'![]({output_svg_name})'
                if maybe_alt != '':
                    result += '{' + maybe_alt.strip() + '}'
                result += '\n'
            else:
                result += (
                    f'![]({output_svg_name})' +
                    '{.fragment .fade-in-then-out fragment-index=' +
                    str(slide_number) + maybe_alt + '}\n\n'
                )
        if not is_overlay:
            if max_slide_number > 1:
                result += '\n:::\n'
                #result += '</div>\n'
        return result

@dataclass
class TikzpictureWithAlt(Tikzpicture):
    def __init__(self, *args):
        self.alt_texts = []
        for item in args:
            if isinstance(item, lark.Token):
                self.contents = item
            elif item.is_whitespace:
                pass
            else:
                self.alt_texts.append(item.inner_text)

@dataclass
class Frametitle(_MyAstItem):
    title: AnyText

    @property
    def inner_text(self):
        return self.title.inner_text

    def render(self, context: RenderContext) -> str:
        return ''

@dataclass
class GenericCommand(_InlineCommand):
    def __init__(self, command, when, *arguments):
        self.command = str(command)
        self.when = when
        self.arguments = arguments

@dataclass
class BlockWithCommand(_InlineCommand):
    def __init__(self, *args):
        if len(args) > 2:
            logging.debug('nested command %s', args)
            self.command = args[0]
            self.arguments = [AnyText(BlockWithCommand(*args[1:]))]
        else:
            self.command = args[0]
            self.arguments = [args[1]]

BareBlock = AnyText

@dataclass
class Item(_MyAstItem):
    when: When
    contents: AnyText

    def __init__(self, when, *args):
        self.when = when
        self.contents = args[-1]

    @property
    def estimated_lines(self) -> float:
        return max(1, self.contents.estimated_lines)

    @property
    def can_be_spanned(self) -> bool:
        return False

    @property
    def inner_text(self) -> str:
        return self.contents.inner_text

    def render(self, context: RenderContext) -> str:
        result = context.indented('\n* ')
        with context.inner(strip_ends=True, extra_indent=3) as inner_context:
            result += self.contents.render(inner_context)
        return result


@dataclass
class Itemize(_MyAstItem):
    items: List[Item]

    def __init__(self, *args):
        self.items = []
        # TODO: ignores optional simple command (e.g. \small) before first \item
        for maybe_item in args:
            if isinstance(maybe_item, Item):
                self.items.append(maybe_item)

    @property
    def estimated_lines(self) -> float:
        return sum(map(attrgetter('estimated_lines'), self.items)) + 0.4 * len(self.items)

    @property
    def can_be_spanned(self) -> bool:
        return False

    def render(self, context: RenderContext) -> str:
        result = ''
        if not context.frame_top:
            result += '\n'
        for item in self.items:
            result += item.render(context)
        result += '\n'
        return result

@dataclass
class TabularLine(_MyAstItem):
    cells: List[AnyText]
    linebreak: object

    def __init__(self, *args):
        self.linebreak = args[-1]
        self.cells = args[:-1]
        logging.debug('linebreak = %s', self.linebreak)
        if isinstance(self.linebreak, AnyText):
            self.cells += (self.linebreak,)
            logging.debug('cells = %s', self.cells)
            self.linebreak = None

    @property
    def inner_text(self) -> str:
        return ' | '.join(map(attrgetter('inner_text'), self.cells))

    def render(self, context: RenderContext) -> str:
        result = '<tr>'
        for cell in self.cells:
            # FIXME: \multicolumn \hline \etc
            result += '<td>'
            with context.inner(strip_ends=True, frame_top=False) as inner_context:
                logging.debug('cell = %s', cell)
                result += cell.render(inner_context)
            result += '</td>'
        result += '</tr>\n'
        return result

TabularLineNonl = TabularLine

@dataclass
class Tabular(_MyAstItem):
    column_types: object
    lines: List[TabularLine]
    end: object

    def __init__(self, column_types, *rest):
        self.column_types = column_types
        self.lines = rest[:-1]
        self.end = rest[-1]
        if isinstance(self.end, TabularLine):
            self.lines += (self.end,)
        elif not self.end.is_whitespace:
            self.lines += (TabularLine(self.end),)
            self.end = None
    
    @property
    def estimated_lines(self) -> float:
        return len(self.lines)

    @property
    def can_be_spanned(self) -> bool:
        return False

    @property
    def inner_text(self) -> str:
        return '\n'.join(map(attrgetter('inner_text'), self.lines))

    def render(self, context: RenderContext) -> str:
        logging.debug('lines = %s', self.lines)
        if context.tt:
            result = context.indented('\n')
            for index, line in enumerate(self.lines):
                result += '<code>'
                for cell in line.cells:
                    with context.inner(strip_ends=True) as inner_context:
                        result += cell.render(inner_context)
                result += '</code>'
                if index != len(self.lines) - 1:
                    result += context.indented('<br />\n')
                else:
                    result += context.indented('\n')
            return result
        else:
            result = context.indented('<table>\n')
            for line in self.lines:
                result += line.render(context)
            result += context.indented('</table>\n')
            return result


@dataclass
class HeldbackFrames(_MyAstItem):
    document: Document

@dataclass
class ScopedDocument(_MyAstItem):
    document: Document

@dataclass
class Frame(_MyAstItem):
    title: None | str
    label: None | str
    contents: AnyText

    @property
    def can_be_spanned(self) -> bool:
        return False

    def __init__(self, *args):
        self.contents = args[-1]
        self.title = ''
        self.label= None
        for item in args[:-1]:
            if item.is_whitespace:
                continue
            if isinstance(item, When):
                continue
            if isinstance(item, OptionalArgument):
                m = re.search('label=([^=,]+)', item.inner_text)
                if m is not None:
                    self.label = m.group(1)
                continue
            self.title += item.inner_text
        if self.title == '':
            for item in self.contents.parts:
                if isinstance(item, Frametitle):
                    self.title = item.inner_text

    def render(self, context) -> str:
        classes = ''
        if self.contents.estimated_lines >= 7:
            classes = ' {.smaller}'
        result = f'\n### {self.title} {classes}\n\n'
        with context.inner(strip_ends=True,
            frame_top=True, frame_title=self.title,
            frame_label=self.label,
            nested_group=True) as inner_context:
            logging.debug('inner context = %s', inner_context)
            result += self.contents.render(inner_context)
        result += '\n'
        return result


@dataclass
class Whitespace(_MyAstItem):
    parts: List[lark.Token]
    has_newline: bool = False
    comment: str = ''

    def __init__(self, *args):
        self.parts = args
        for item in args:
            if item.type == 'COMMENT':
                self.comment += item.value[1:].strip()
            elif item.type == 'NEWLINE':
                self.has_newline = True

    @property
    def is_whitespace(self):
        return True

    @property
    def inner_text(self) -> str:
        if self.has_newline:
            return '\n'
        else:
            return ' '

    def render(self, context: RenderContext) -> str:
        if len(self.comment) > 0:
            return f'<!-- {self.comment} -->'
        else:
            return ' '

@dataclass
class OutsideCommand(_MyAstItem):
    command: str
    when: None | When
    arguments: List[AnyText]

    def __init__(self, command, *arguments):
        logging.debug('OutsideCommand: %s %s', command, arguments)
        self.command = str(command)
        self.arguments = []
        for item in arguments:
            if isinstance(item, When):
                self.when = item
            elif isinstance(item, AnyText):
                self.arguments.append(item)
            else:
                self.command += str(item)

    def render(self, context: RenderContext) -> str:
        if self.command == r'\usetikzlibrary':
            context.add_tikz_libraries(self.arguments[0].inner_text.split(','))
            return ''
        elif self.command == r'\input':
            logging.debug('input %s', self.arguments)
            filename = self.arguments[0].inner_text
            if filename in ('../common/listingsLib', '../common/listingsLib.tex'):
                return '<!-- \\input{' + filename + '} -->'
            input_file = context.base_output_path.parent / filename
            input_file = input_file.with_name(
                '_' + input_file.name
            )
            if not input_file.name.endswith('.tex'):
                input_file.with_name(input_file.name + '.tex')
            input_file = input_file.with_suffix('.qmd')
            return '\n{{< include /' + \
                str(input_file.resolve().relative_to(context.base_quarto_path.resolve())) + \
                ' >}}\n'
        elif self.command == r'\section' or self.command == r'\section*':
            return f'\n# {self.arguments[0].inner_text} ' + '{visibility="hidden"}\n'
        elif self.command == r'\subsection':
            return f'\n## {self.arguments[0].inner_text} ' + '{visibility="hidden"}\n'
        elif self.command == r'\subsubsection':
            return f'\n## {self.arguments[0].inner_text}' + '{visibility="hidden"}\n'
        elif self.command in (r'\iftoggle', r'\setbeamertemplate', r'\titlepage',
                              r'\title', r'\date'):
            result = f'\n<!-- {self.command}('
            result += ','.join(map(attrgetter('inner_text'), self.arguments))
            result += ') -->\n'
            return result
        else:
            result = f'\n### {self.command[1:]}('
            if self.when is not None and self.when.raw_when is not None:
                result += self.when.raw_when
            result += ','.join(map(attrgetter('inner_text'), self.arguments))
            result += ')\n'
            return result


@dataclass
class GenericEnvironment(_MyAstItem):
    begin_generic: lark.Token
    contents: AnyText
    end_generic: lark.Token

    def render(self, context: RenderContext) -> str:
        result = '\n```\n'
        result += str(self.begin_generic) + '\n'
        with context.inner(pre=True) as inner_context:
            result += self.contents.render(inner_context)
        result += '\n'
        result += str(self.end_generic)
        result += '\n```\n'
        return result

@dataclass
class OutsideEnvironment(GenericEnvironment):
    def render(self, context: RenderContext) -> str:
        result = '###\n'
        result += super().render(context)
        result += '\n'
        return result

@dataclass
class AnyEmptyItem(_MyAstItem):
    contents: List[_MyAstItem]

    def __init__(self, *contents):
        logging.debug('AnyEmptyItem: %s', contents)
        self.contents = contents

    @property
    def inner_text(self):
        return ''

@dataclass
class Document(_MyAstItem):
    parts: List[Frame | AnyEmptyItem]
    frame_count: int

    def __init__(self, *args):
        self.parts = []
        for part in args:
            if isinstance(part, HeldbackFrames) or isinstance(part, ScopedDocument):
                self.parts += part.document.parts
            else:
                self.parts.append(part)
        self.frame_count = 0
        for part in self.parts:
            if isinstance(part, Frame):
                self.frame_count += 1

    @property
    def inner_text(self) -> str:
        return ''.join(map(attrgetter('inner_text'), self.parts))

    def render(self, context: RenderContext) -> str:
        context.frame_count = self.frame_count
        return ''.join(map(methodcaller('render', context), self.parts))



class ToAST(lark.Transformer):
    def ANY(self, args):
        as_markdown = re.sub(r'[<\[\\]', lambda m: '\\' + m.group(0), args[0])
        return _RawString(args[0], as_markdown)

    def LINEBREAK(self, args):
        return _RawString('\n', '<br>')

    def SIMPLE_ESCAPED(self, args):
        if args[1] == '&':
            return _RawString('&', '&amp;')
        elif args[1] == '$':
            return _RawString('$', r'\$')
        elif args[1] == '\\':
            return _RawString('\\', '\\\\')
        else:
            return _RawString(args[1])

    def NBSP(self, args):
        return _RawString(' ', '&nbsp;')

    def DISPLAYMATH(self, args):
        return _RawString(args, args)

    def INLINEMATH(self, args):
        return _RawString(args, args)

    def UMLAT(self, args):
        base_str = args[-1] + "\N{COMBINING DIAERESIS}"
        base_str = unicodedata.normalize('NFC', base_str)
        return _RawString(base_str, base_str)

    def dquote(self, args):
        new_args = [_RawString('\N{left double quotation mark}')] + \
           args + \
           [_RawString('\N{right double quotation mark}')]
        return AnyText(*new_args)

    def squote(self, args):
        new_args = [_RawString('\N{left single quotation mark}')] + \
            args + \
            [_RawString('\N{right single quotation mark}')]
        return AnyText(*new_args)

    def start(self, args):
        return args

    def square_bracket(self, args):
        return _RawString('[', '[')
    
    def end_square_bracket(self, args):
        return _RawString(']', ']')

def parse_and_render_file(input_file: Path, output_file: Path) -> str:
    global GRAMMAR
    lark = Lark(GRAMMAR, start='start', strict=True)
    result = lark.parse(input_file.read_text())
    #result = lark.parse(r'''\begin{frame}\end{frame}''')

    logging.debug('parsed as %s', result)

    #print(result)

    global current_module
    transformer = ast_utils.create_transformer(current_module, ToAST())

    result = transformer.transform(result)
    logging.debug('transformed as %s', result)
    return result[0].render(
        RenderContext(
            base_input_path=input_file,
            base_output_path=output_file,
            base_quarto_path=output_file.parent.parent
        )
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = parse_and_render_file(args.input, args.output)
    args.output.parent.mkdir(exist_ok=True)
    args.output.write_text(result)

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    logging.basicConfig(level=logging.DEBUG)
    main()

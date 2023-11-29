from __future__ import annotations

import itertools
import textwrap
from collections.abc import Iterator
from typing import Any

from .. import grammars
from ..collections import OrderedSet as oset
from ..exceptions import CodegenError
from ..mixins.indent import IndentPrintMixin
from ..util import compress_seq, safe_name, trim
from ..walkers import NodeWalker

HEADER = """\
    #!/usr/bin/env python3

    # WARNING: CAVEAT UTILITOR
    #
    #  This file was automatically generated by TatSu.
    #
    #     https://pypi.python.org/pypi/tatsu/
    #
    #  Any changes you make to it will be overwritten the next time
    #  the file is generated.

    # ruff: noqa: C405, I001, F401, SIM117

    import sys
    from pathlib import Path

    from tatsu.buffering import Buffer
    from tatsu.parsing import Parser
    from tatsu.parsing import tatsumasu
    from tatsu.parsing import leftrec, nomemo, isname
    from tatsu.infos import ParserConfig
    from tatsu.util import re, generic_main
"""

FOOTER = """\
def main(filename, **kwargs):
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        text = Path(filename).read_text()
    parser = {name}Parser()
    return parser.parse(
        text,
        filename=filename,
        **kwargs,
    )


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, {name}Parser, name='{name}')
    data = asjson(ast)
    print(json.dumps(data, indent=2))
"""


class PythonCodeGenerator(IndentPrintMixin, NodeWalker):
    _counter: Iterator[int] = itertools.count()

    def __init__(self, parser_name: str = ''):
        super().__init__()
        self.parser_name = parser_name

    @classmethod
    def _next_n(cls):
        return next(cls._counter)

    @classmethod
    def _reset_counter(cls):
        cls._counter = itertools.count()

    def walk_default(self, node: Any):
        return node

    def walk_Grammar(self, grammar: grammars.Grammar):
        parser_name = self.parser_name or grammar.name
        self.print(HEADER)
        self.print()
        self.print()

        self._gen_keywords(grammar)
        self._gen_buffering(grammar)
        self._gen_parsing(grammar)

        self.print()
        self.print(FOOTER.format(name=parser_name))

    def walk_Rule(self, rule: grammars.Rule):
        def param_repr(p):
            if isinstance(p, int | float):
                return str(p)
            else:
                return repr(p.split('::')[0])

        self._reset_counter()
        params = kwparams = ''
        if rule.params:
            params = ', '.join(
                param_repr(self.walk(p)) for p in rule.params
            )
        if rule.kwparams:
            kwparams = ', '.join(
                f'{k}={param_repr(self.walk(v))}'
                for k, v in rule.kwparams.items()
            )

        if params and kwparams:
            params = params + ', ' + kwparams
        elif kwparams:
            params = kwparams

        leftrec = '\n@leftrec' if rule.is_leftrec else ''
        nomemo = (
            '\n@nomemo'
            if not rule.is_memoizable and not leftrec
            else ''
        )
        isname = '\n@isname' if rule.is_name else ''

        self.print()
        self.print(
            f"""
            @tatsumasu({params})\
            {leftrec}\
            {nomemo}\
            {isname}
            def _{rule.name}_(self):
            """,
        )
        with self.indent():
            self.print(self.walk(rule.exp))
            if not isinstance(rule.exp, grammars.Choice):
                self._gen_defines_declaration(rule)


    def walk_BasedRule(self, rule: grammars.BasedRule):
        # FIXME: the following override is to not alter the previous codegen
        rule.exp = rule.rhs
        self.walk_Rule(rule)

    def walk_RuleRef(self, ref: grammars.RuleRef):
        self.print(f'self._{ref.name}_()')

    def walk_RuleInclude(self, include: grammars.RuleInclude):
        self.walk(include.rule.exp)

    def walk_Void(self, void: grammars.Void):
        self.print('self._void()')

    def walk_Any(self, any: grammars.Any):
        self.print('self._any()')

    def walk_Fail(self, fail: grammars.Fail):
        self.print('self._fail()')

    def walk_Cut(self, cut: grammars.Cut):
        self.print('self._cut()')

    def walk_Comment(self, comment: grammars.Comment):
        lines = '\n'.join(f'# {c!s}' for c in comment.comment.splitlines())
        self.print(f'\n{lines}\n')

    def walk_EOLComment(self, comment: grammars.EOLComment):
        self.walk_Comment(comment)

    def walk_EOF(self, eof: grammars.EOF):
        self.print('self._check_eof()')

    def walk_Group(self, group: grammars.Group):
        self.print('with self._group():')
        with self.indent():
            self.walk(group.exp)

    def walk_Token(self, token: grammars.Token):
        self.print(f'self._token({token.token!r})')

    def walk_Constant(self, constant: grammars.Constant):
        self.print(f'self._constant({constant.literal!r})')

    def walk_Alert(self, alert: grammars.Alert):
        self.print(f'self._alert({alert.literal!r}, {alert.level})')

    def walk_Pattern(self, pattern: grammars.Pattern):
        self.print(f'self._pattern({pattern.pattern!r})')

    def walk_Lookahead(self, lookahead: grammars.Lookahead):
        self.print('with self._if():')
        with self.indent():
            self.walk(lookahead.exp)

    def walk_NegativeLookahead(self, lookahead: grammars.NegativeLookahead):
        self.print('with self._ifnot():')
        with self.indent():
            self.walk(lookahead.exp)

    def walk_Sequence(self, seq: grammars.Sequence):
        self.walk(seq.sequence)
        self._gen_defines_declaration(seq)

    def walk_Choice(self, choice: grammars.Choice):
        if len(choice.options) == 1:
            self.walk(choice.options[0])
            return

        firstset = choice.lookahead_str()
        if firstset:
            msglines = textwrap.wrap(firstset, width=40)
            error = ['expecting one of: ', *msglines]
        else:
            error = ['no available options']
        errors = '\n'.join(repr(e) for e in error)

        self.print('with self._choice():')
        with self.indent():
            self.walk(choice.options)
            self.print('self._error(')
            with self.indent():
                self.print(errors)
            self.print(')')

    def walk_Option(self, option: grammars.Option):
        self.print('with self._option():')
        with self.indent():
            self.walk(option.exp)

    def walk_Optional(self, optional: grammars.Optional):
        self.print('with self._optional():')
        with self.indent():
            self.walk(optional.exp)

    def walk_EmptyClosure(self, closure: grammars.EmptyClosure):
        self.print('self._empty_closure()')

    def walk_Closure(self, closure: grammars.Closure):
        n = self._gen_block(closure.exp)
        self.print(f'self._closure(block{n})')

    def walk_PositiveClosure(self, closure: grammars.PositiveClosure):
        n = self._gen_block(closure.exp)
        self.print(f'self._positive_closure(block{n})')

    def walk_Join(self, join: grammars.Join):
        n = self._gen_block(join.sep, name='sep')
        n = self._gen_block(join.exp)
        self.print(f'self._join(block{n}, sep{n})')

    def walk_PositiveJoin(self, join: grammars.PositiveJoin):
        n = self._gen_block(join.sep, name='sep')
        n = self._gen_block(join.exp)
        self.print(f'self._positive_join(block{n}, sep{n})')

    def walk_LeftJoin(self, join: grammars.LeftJoin):
        n = self._gen_block(join.sep, name='sep')
        n = self._gen_block(join.exp)
        self.print(f'self._left_join(block{n}, sep{n})')

    def walk_RightJoin(self, join: grammars.RightJoin):
        n = self._gen_block(join.sep, name='sep')
        n = self._gen_block(join.exp)
        self.print(f'self._right_join(block{n}, sep{n})')

    def walk_Gather(self, gather: grammars.Gather):
        m = self._gen_block(gather.sep, name='sep')
        n = self._gen_block(gather.exp)
        self.print(f'self._gather(block{n}, sep{m})')

    def walk_PositiveGather(self, gather: grammars.PositiveGather):
        m = self._gen_block(gather.sep, name='sep')
        n = self._gen_block(gather.exp)
        self.print(f'self._positive_gather(block{n}, sep{m})')

    def walk_SkipTo(self, skipto: grammars.SkipTo):
        n = self._gen_block(skipto.exp)
        self.print(f'self._skip_to(block{n})')


    def walk_Named(self, named: grammars.Named):
        self.walk(named.exp)
        self.print(f"self.name_last_node('{named.name}')")

    def walk_NamedList(self, named: grammars.Named):
        self.walk(named.exp)
        self.print(f"self.add_last_node_to_name('{named.name}')")

    def walk_Override(self, override: grammars.Override):
        self.walk_Named(override)

    def walk_OverrideList(self, override: grammars.OverrideList):
        self.walk_NamedList(override)

    def walk_Special(self, special: grammars.Special):
        pass

    def _gen_keywords(self, grammar: grammars.Grammar):
        keywords = [str(k) for k in grammar.keywords if k is not None]
        if not keywords:
            self.print('KEYWORDS: set[str] = set()')
        else:
            keywords_str = '\n'.join(f'    {k!r},' for k in keywords)
            keywords_str = '{\n%s\n}' % keywords_str
            self.print(f'KEYWORDS: set[str] = {keywords_str}')

        self.print()
        self.print()


    def _gen_init(self, grammar: grammars.Grammar):
        start = grammar.config.start or grammar.rules[0].name
        self.print(
            f'''
                    config = ParserConfig.new(
                        config,
                        owner=self,
                        whitespace={grammar.config.whitespace!r},
                        nameguard={grammar.config.nameguard},
                        ignorecase={grammar.config.ignorecase},
                        namechars={grammar.config.namechars or None},
                        parseinfo={grammar.config.parseinfo},
                        comments_re={grammar.config.comments_re!r},
                        eol_comments_re={grammar.config.eol_comments_re!r},
                        keywords=KEYWORDS,
                        start={start!r},
                    )
                    config = config.replace(**settings)
                    ''',
        )
        self.print()

    def _gen_buffering(self, grammar: grammars.Grammar):
        self.print(f'class {self.parser_name}Buffer(Buffer):')

        with self.indent():
            self.print('def __init__(self, text, /, config: ParserConfig | None = None, **settings):')
            with self.indent():
                self._gen_init(grammar)
                self.print('super().__init__(text, config=config)')
        self.print()


    def _gen_parsing(self, grammar: grammars.Grammar):
        self.print(f'class {self.parser_name}Parser(Parser):')
        with self.indent():
            self.print('def __init__(self, /, config: ParserConfig | None = None, **settings):')
            with self.indent():
                self._gen_init(grammar)
                self.print('super().__init__(config=config)')
            self.walk(grammar.rules)

    def _gen_defines_declaration(self, node: grammars.Model):
        defines = compress_seq(node.defines())
        ldefs = oset(safe_name(d) for d, value in defines if value)
        sdefs = oset(
            safe_name(d)
            for d, value in defines
            if not value and d not in ldefs
        )

        if not (sdefs or ldefs):
            return

        sdefs_str = ', '.join(sorted(repr(d) for d in sdefs))
        ldefs_str = ', '.join(sorted(repr(d) for d in ldefs))

        if not ldefs:
            self.print(f'self._define([{sdefs_str}], [{ldefs_str}])')
        else:
            self.print('self._define(')
            with self.indent():
                self.print(f'[{sdefs_str}],')
                self.print(f'[{ldefs_str}],')
            self.print(')')

    def _gen_block(self, exp: grammars.Model, name='block'):
        if () in exp.lookahead():
            raise CodegenError(f'{self.node} may repeat empty sequence')

        n = self._next_n()
        self.print()
        self.print(f'def {name}{n}():')
        with self.indent():
            self.walk(exp)

        return n

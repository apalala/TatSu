from __future__ import annotations

from .. import grammars
from ..mixins.indent import IndentPrintMixin
from ..util import trim
from ..walkers import NodeWalker


HEADER= """\
    #!/usr/bin/env python

    # WARNING:
    #
    #  CAVEAT UTILITOR
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


class PythonCodeGenerator(IndentPrintMixin, NodeWalker):

    def print(self, *args, **kwargs):
        args = [trim(arg) for arg in args]
        super().print(*args, **kwargs)

    def walk_Grammar(self, grammar: grammars.Grammar):
        self.print(HEADER)
        self.print()
        self.print()

        self._gen_keywords(grammar)
        self._gen_buffering(grammar)

        self.print(
            '''
            ** AT GRAMMAR
            '''
        )

    def _gen_keywords(self, grammar: grammars.Grammar):
        keywords = [str(k) for k in grammar.keywords if k is not None]
        if not keywords:
            self.print('KEYWORDS: set[str] = set()')
        else:
            keywords = '\n'.join(f'    {k!r},' for k in keywords)
            keywords = '{\n%s\n}' % keywords
            self.print(f'KEYWORDS: set[str] = {keywords}')

        self.print()
        self.print()

    def _gen_buffering(self, grammar: grammars.Grammar):
        self.print(f'class {grammar.name}Buffer(Buffer):')
        start = grammar.config.start or grammar.rules[0].name

        with self.indent():
            self.print('def __init__(self, text, /, config: ParserConfig | None = None, **settings):')
            with self.indent():
                self.print(
                    f'''
                    config = ParserConfig.new(
                        config,
                        owner=self,
                        whitespace={grammar.config.whitespace},
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
                    super().__init__(text, config=config)
                    '''
                )

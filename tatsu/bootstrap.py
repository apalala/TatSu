#!/usr/bin/env python

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.

# ruff: noqa: I001, SIM117

import sys
from pathlib import Path

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu
from tatsu.parsing import leftrec, nomemo, isname  # noqa: F401
from tatsu.infos import ParserConfig
from tatsu.util import re, generic_main  # noqa: F401


KEYWORDS: set[str] = {
    'None',
}


class EBNFBootstrapBuffer(Buffer):
    def __init__(self, text, /, config: ParserConfig | None = None, **settings):
        config = ParserConfig.new(
            config,
            owner=self,
            whitespace=None,
            nameguard=None,
            ignorecase=False,
            namechars='',
            parseinfo=True,
            comments_re='(?sm)[(][*](?:.|\\n)*?[*][)]',
            eol_comments_re='#[^\\n]*$',
            keywords=KEYWORDS,
            start='start',
        )
        config = config.replace(**settings)
        super().__init__(text, config=config)


class EBNFBootstrapParser(Parser):
    def __init__(self, /, config: ParserConfig | None = None, **settings):
        config = ParserConfig.new(
            config,
            owner=self,
            whitespace=None,
            nameguard=None,
            ignorecase=False,
            namechars='',
            parseinfo=True,
            comments_re='(?sm)[(][*](?:.|\\n)*?[*][)]',
            eol_comments_re='#[^\\n]*$',
            keywords=KEYWORDS,
            start='start',
        )
        config = config.replace(**settings)
        super().__init__(config=config)

    @tatsumasu()
    def _start_(self):
        self._grammar_()

    @tatsumasu('Grammar')
    def _grammar_(self):
        self._constant('TATSU')
        self.name_last_node('title')

        def block1():
            with self._choice():
                with self._option():
                    self._directive_()
                    self.add_last_node_to_name('directives')
                with self._option():
                    self._keyword_()
                    self.add_last_node_to_name('keywords')
                self._error(
                    'expecting one of: '
                    '<directive> <keyword>'  # noqa: COM812
                )
        self._closure(block1)
        self._rule_()
        self.add_last_node_to_name('rules')

        def block6():
            with self._choice():
                with self._option():
                    self._rule_()
                    self.add_last_node_to_name('rules')
                with self._option():
                    self._keyword_()
                    self.add_last_node_to_name('keywords')
                self._error(
                    'expecting one of: '
                    '<keyword> <rule>'  # noqa: COM812
                )
        self._closure(block6)
        self._check_eof()

        self._define(
            ['title'],
            ['directives', 'keywords', 'rules'],
        )

    @tatsumasu()
    def _directive_(self):
        self._token('@@')
        with self._ifnot():
            self._token('keyword')
        self._cut()
        with self._group():
            with self._choice():
                with self._option():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('comments')
                            with self._option():
                                self._token('eol_comments')
                            self._error(
                                'expecting one of: '
                                "'comments' 'eol_comments'"  # noqa: COM812
                            )
                    self.name_last_node('name')
                    self._cut()
                    self._cut()
                    self._token('::')
                    self._cut()
                    self._regex_()
                    self.name_last_node('value')

                    self._define(
                        ['name', 'value'],
                        [],
                    )
                with self._option():
                    with self._group():
                        self._token('whitespace')
                    self.name_last_node('name')
                    self._cut()
                    self._cut()
                    self._token('::')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._regex_()
                            with self._option():
                                self._token('None')
                            with self._option():
                                self._token('False')
                            with self._option():
                                self._constant('None')
                            self._error(
                                'expecting one of: '
                                "'False' 'None' <regex>"  # noqa: COM812
                            )
                    self.name_last_node('value')

                    self._define(
                        ['name', 'value'],
                        [],
                    )
                with self._option():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('nameguard')
                            with self._option():
                                self._token('ignorecase')
                            with self._option():
                                self._token('left_recursion')
                            with self._option():
                                self._token('parseinfo')
                            self._error(
                                'expecting one of: '
                                "'ignorecase' 'left_recursion'"
                                "'nameguard' 'parseinfo'"  # noqa: COM812
                            )
                    self.name_last_node('name')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('::')
                                self._cut()
                                self._boolean_()
                                self.name_last_node('value')

                                self._define(
                                    ['value'],
                                    [],
                                )
                            with self._option():
                                self._constant(True)
                                self.name_last_node('value')
                            self._error(
                                'expecting one of: '
                                "'::'"  # noqa: COM812
                            )

                    self._define(
                        ['name', 'value'],
                        [],
                    )
                with self._option():
                    with self._group():
                        self._token('grammar')
                    self.name_last_node('name')
                    self._cut()
                    self._token('::')
                    self._cut()
                    self._word_()
                    self.name_last_node('value')

                    self._define(
                        ['name', 'value'],
                        [],
                    )
                with self._option():
                    with self._group():
                        self._token('namechars')
                    self.name_last_node('name')
                    self._cut()
                    self._token('::')
                    self._cut()
                    self._string_()
                    self.name_last_node('value')

                    self._define(
                        ['name', 'value'],
                        [],
                    )
                self._error(
                    'expecting one of: '
                    "'comments' 'eol_comments' 'grammar'"
                    "'ignorecase' 'left_recursion'"
                    "'namechars' 'nameguard' 'parseinfo'"
                    "'whitespace'"  # noqa: COM812
                )
        self._cut()

        self._define(
            ['name', 'value'],
            [],
        )

    @tatsumasu()
    def _keywords_(self):

        def block0():
            self._keywords_()
        self._positive_closure(block0)

    @tatsumasu()
    def _keyword_(self):
        self._token('@@keyword')
        self._cut()
        self._token('::')
        self._cut()

        def block0():
            self._literal_()
            self.add_last_node_to_name('@')
            with self._ifnot():
                with self._group():
                    with self._choice():
                        with self._option():
                            self._token(':')
                        with self._option():
                            self._token('=')
                        self._error(
                            'expecting one of: '
                            "':' '='"  # noqa: COM812
                        )
        self._closure(block0)

    @tatsumasu()
    def _paramdef_(self):
        with self._choice():
            with self._option():
                self._token('::')
                self._cut()
                self._params_()
                self.name_last_node('params')

                self._define(
                    ['params'],
                    [],
                )
            with self._option():
                self._token('(')
                self._cut()
                with self._group():
                    with self._choice():
                        with self._option():
                            self._kwparams_()
                            self.name_last_node('kwparams')
                        with self._option():
                            self._params_()
                            self.name_last_node('params')
                            self._token(',')
                            self._cut()
                            self._kwparams_()
                            self.name_last_node('kwparams')

                            self._define(
                                ['kwparams', 'params'],
                                [],
                            )
                        with self._option():
                            self._params_()
                            self.name_last_node('params')
                        self._error(
                            'expecting one of: '
                            '<kwparams> <params>'  # noqa: COM812
                        )
                self._token(')')

                self._define(
                    ['kwparams', 'params'],
                    [],
                )
            self._error(
                'expecting one of: '
                "'(' '::'"  # noqa: COM812
            )

    @tatsumasu('Rule')
    def _rule_(self):

        def block1():
            self._decorator_()
        self._closure(block1)
        self.name_last_node('decorators')
        self._name_()
        self.name_last_node('name')
        self._cut()
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('::')
                    self._cut()
                    self._params_()
                    self.name_last_node('params')

                    self._define(
                        ['params'],
                        [],
                    )
                with self._option():
                    self._token('(')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._kwparams_()
                                self.name_last_node('kwparams')
                            with self._option():
                                self._params_()
                                self.name_last_node('params')
                                self._token(',')
                                self._cut()
                                self._kwparams_()
                                self.name_last_node('kwparams')

                                self._define(
                                    ['kwparams', 'params'],
                                    [],
                                )
                            with self._option():
                                self._params_()
                                self.name_last_node('params')
                            self._error(
                                'expecting one of: '
                                '<kwparams> <params>'  # noqa: COM812
                            )
                    self._token(')')

                    self._define(
                        ['kwparams', 'params'],
                        [],
                    )
                self._error(
                    'expecting one of: '
                    "'(' '::'"  # noqa: COM812
                )
        with self._optional():
            self._token('<')
            self._cut()
            self._known_name_()
            self.name_last_node('base')

            self._define(
                ['base'],
                [],
            )
        self._token('=')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token(';')
        self._cut()

        self._define(
            ['base', 'decorators', 'exp', 'kwparams', 'name', 'params'],
            [],
        )

    @tatsumasu()
    def _decorator_(self):
        self._token('@')
        with self._ifnot():
            self._token('@')
        self._cut()
        with self._group():
            with self._choice():
                with self._option():
                    self._token('override')
                with self._option():
                    self._token('name')
                with self._option():
                    self._token('nomemo')
                self._error(
                    'expecting one of: '
                    "'name' 'nomemo' 'override'"  # noqa: COM812
                )
        self.name_last_node('@')

    @tatsumasu()
    def _params_(self):
        self._first_param_()
        self.add_last_node_to_name('@')

        def block1():
            self._token(',')
            self._literal_()
            self.add_last_node_to_name('@')
            with self._ifnot():
                self._token('=')
            self._cut()
        self._closure(block1)

    @tatsumasu()
    def _first_param_(self):
        with self._choice():
            with self._option():
                self._path_()
            with self._option():
                self._literal_()
            self._error(
                'expecting one of: '
                '(?!\\d)\\w+(?:::(?!\\d)\\w+)+ <boolean>'
                '<float> <hex> <int> <literal> <null>'
                '<path> <raw_string> <string> <word>'  # noqa: COM812
            )

    @tatsumasu()
    def _kwparams_(self):

        def sep0():
            self._token(',')

        def block0():
            self._pair_()
        self._positive_gather(block0, sep0)

    @tatsumasu()
    def _pair_(self):
        self._word_()
        self.add_last_node_to_name('@')
        self._token('=')
        self._cut()
        self._literal_()
        self.add_last_node_to_name('@')

    @tatsumasu()
    def _expre_(self):
        with self._choice():
            with self._option():
                self._choice_()
            with self._option():
                self._sequence_()
            self._error(
                'expecting one of: '
                "'|' <choice> <element> <option>"
                '<sequence>'  # noqa: COM812
            )

    @tatsumasu('Choice')
    def _choice_(self):
        with self._optional():
            self._token('|')
            self._cut()
        self._option_()
        self.add_last_node_to_name('@')

        def block1():
            self._token('|')
            self._cut()
            self._option_()
            self.add_last_node_to_name('@')
        self._positive_closure(block1)

    @tatsumasu('Option')
    def _option_(self):
        self._sequence_()
        self.name_last_node('@')

    @tatsumasu('Sequence')
    def _sequence_(self):

        def block1():
            self._element_()
        self._positive_closure(block1)
        self.name_last_node('sequence')

    @tatsumasu()
    def _element_(self):
        with self._choice():
            with self._option():
                self._rule_include_()
            with self._option():
                self._named_()
            with self._option():
                self._override_()
            with self._option():
                self._term_()
            self._error(
                'expecting one of: '
                "'>' <atom> <closure> <empty_closure>"
                '<gather> <group> <join> <left_join>'
                '<lookahead> <named> <named_list>'
                '<named_single> <negative_lookahead>'
                '<optional> <override> <override_list>'
                '<override_single>'
                '<override_single_deprecated>'
                '<positive_closure> <right_join>'
                '<rule_include> <skip_to> <special>'
                '<term> <void>'  # noqa: COM812
            )

    @tatsumasu('RuleInclude')
    def _rule_include_(self):
        self._token('>')
        self._cut()
        self._known_name_()
        self.name_last_node('@')

    @tatsumasu()
    def _named_(self):
        with self._choice():
            with self._option():
                self._named_list_()
            with self._option():
                self._named_single_()
            self._error(
                'expecting one of: '
                '<name> <named_list> <named_single>'  # noqa: COM812
            )

    @tatsumasu('NamedList')
    def _named_list_(self):
        self._name_()
        self.name_last_node('name')
        self._token('+:')
        self._cut()
        self._term_()
        self.name_last_node('exp')

        self._define(
            ['exp', 'name'],
            [],
        )

    @tatsumasu('Named')
    def _named_single_(self):
        self._name_()
        self.name_last_node('name')
        self._token(':')
        self._cut()
        self._term_()
        self.name_last_node('exp')

        self._define(
            ['exp', 'name'],
            [],
        )

    @tatsumasu()
    def _override_(self):
        with self._choice():
            with self._option():
                self._override_list_()
            with self._option():
                self._override_single_()
            with self._option():
                self._override_single_deprecated_()
            self._error(
                'expecting one of: '
                "'@' '@+:' '@:' <override_list>"
                '<override_single>'
                '<override_single_deprecated>'  # noqa: COM812
            )

    @tatsumasu('OverrideList')
    def _override_list_(self):
        self._token('@+:')
        self._cut()
        self._term_()
        self.name_last_node('@')

    @tatsumasu('Override')
    def _override_single_(self):
        self._token('@:')
        self._cut()
        self._term_()
        self.name_last_node('@')

    @tatsumasu('Override')
    def _override_single_deprecated_(self):
        self._token('@')
        self._cut()
        self._term_()
        self.name_last_node('@')

    @tatsumasu()
    def _term_(self):
        with self._choice():
            with self._option():
                self._void_()
            with self._option():
                self._gather_()
            with self._option():
                self._join_()
            with self._option():
                self._left_join_()
            with self._option():
                self._right_join_()
            with self._option():
                self._group_()
            with self._option():
                self._empty_closure_()
            with self._option():
                self._positive_closure_()
            with self._option():
                self._closure_()
            with self._option():
                self._optional_()
            with self._option():
                self._special_()
            with self._option():
                self._skip_to_()
            with self._option():
                self._lookahead_()
            with self._option():
                self._negative_lookahead_()
            with self._option():
                self._atom_()
            self._error(
                'expecting one of: '
                "'!' '&' '(' '()' '->' '?(' '[' '{'"
                '<alert> <atom> <call> <closure>'
                '<constant> <cut> <cut_deprecated>'
                '<empty_closure> <eof> <gather> <group>'
                '<join> <left_join> <lookahead>'
                '<negative_lookahead> <optional>'
                '<pattern> <positive_closure>'
                '<right_join> <separator> <skip_to>'
                '<special> <token> <void>'  # noqa: COM812
            )

    @tatsumasu('Group')
    def _group_(self):
        self._token('(')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token(')')
        self._cut()

        self._define(
            ['exp'],
            [],
        )

    @tatsumasu()
    def _gather_(self):
        with self._if():
            with self._group():
                self._separator_()
                self._token('.{')
        self._cut()
        with self._group():
            with self._choice():
                with self._option():
                    self._positive_gather_()
                with self._option():
                    self._normal_gather_()
                self._error(
                    'expecting one of: '
                    '<normal_gather> <positive_gather>'  # noqa: COM812
                )

    @tatsumasu('PositiveGather')
    def _positive_gather_(self):
        self._separator_()
        self.name_last_node('sep')
        self._token('.{')
        self._expre_()
        self.name_last_node('exp')
        self._token('}')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('+')
                with self._option():
                    self._token('-')
                self._error(
                    'expecting one of: '
                    "'+' '-'"  # noqa: COM812
                )
        self._cut()

        self._define(
            ['exp', 'sep'],
            [],
        )

    @tatsumasu('Gather')
    def _normal_gather_(self):
        self._separator_()
        self.name_last_node('sep')
        self._token('.{')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token('}')
        with self._optional():
            self._token('*')
            self._cut()
        self._cut()

        self._define(
            ['exp', 'sep'],
            [],
        )

    @tatsumasu()
    def _join_(self):
        with self._if():
            with self._group():
                self._separator_()
                self._token('%{')
        self._cut()
        with self._group():
            with self._choice():
                with self._option():
                    self._positive_join_()
                with self._option():
                    self._normal_join_()
                self._error(
                    'expecting one of: '
                    '<normal_join> <positive_join>'  # noqa: COM812
                )

    @tatsumasu('PositiveJoin')
    def _positive_join_(self):
        self._separator_()
        self.name_last_node('sep')
        self._token('%{')
        self._expre_()
        self.name_last_node('exp')
        self._token('}')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('+')
                with self._option():
                    self._token('-')
                self._error(
                    'expecting one of: '
                    "'+' '-'"  # noqa: COM812
                )
        self._cut()

        self._define(
            ['exp', 'sep'],
            [],
        )

    @tatsumasu('Join')
    def _normal_join_(self):
        self._separator_()
        self.name_last_node('sep')
        self._token('%{')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token('}')
        with self._optional():
            self._token('*')
            self._cut()
        self._cut()

        self._define(
            ['exp', 'sep'],
            [],
        )

    @tatsumasu('LeftJoin')
    def _left_join_(self):
        self._separator_()
        self.name_last_node('sep')
        self._token('<{')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token('}')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('+')
                with self._option():
                    self._token('-')
                self._error(
                    'expecting one of: '
                    "'+' '-'"  # noqa: COM812
                )
        self._cut()

        self._define(
            ['exp', 'sep'],
            [],
        )

    @tatsumasu('RightJoin')
    def _right_join_(self):
        self._separator_()
        self.name_last_node('sep')
        self._token('>{')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token('}')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('+')
                with self._option():
                    self._token('-')
                self._error(
                    'expecting one of: '
                    "'+' '-'"  # noqa: COM812
                )
        self._cut()

        self._define(
            ['exp', 'sep'],
            [],
        )

    @tatsumasu()
    def _separator_(self):
        with self._choice():
            with self._option():
                self._group_()
            with self._option():
                self._token_()
            with self._option():
                self._constant_()
            with self._option():
                self._any_()
            with self._option():
                self._pattern_()
            self._error(
                'expecting one of: '
                "'(' '/./' '`' <any> <constant> <group>"
                '<pattern> <raw_string> <regexes>'
                '<string> <token>'  # noqa: COM812
            )

    @tatsumasu('PositiveClosure')
    def _positive_closure_(self):
        self._token('{')
        self._expre_()
        self.name_last_node('@')
        self._token('}')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('-')
                with self._option():
                    self._token('+')
                self._error(
                    'expecting one of: '
                    "'+' '-'"  # noqa: COM812
                )
        self._cut()

    @tatsumasu('Closure')
    def _closure_(self):
        self._token('{')
        self._expre_()
        self.name_last_node('@')
        self._token('}')
        with self._optional():
            self._token('*')
        self._cut()

    @tatsumasu('EmptyClosure')
    def _empty_closure_(self):
        self._token('{')
        self._void()
        self.name_last_node('@')
        self._token('}')

    @tatsumasu('Optional')
    def _optional_(self):
        self._token('[')
        self._cut()
        self._expre_()
        self.name_last_node('@')
        self._token(']')
        self._cut()

    @tatsumasu('Special')
    def _special_(self):
        self._token('?(')
        self._cut()
        self._pattern('.*?(?!\\)\\?)')
        self.name_last_node('@')
        self._token(')?')
        self._cut()

    @tatsumasu('Lookahead')
    def _lookahead_(self):
        self._token('&')
        self._cut()
        self._term_()
        self.name_last_node('@')

    @tatsumasu('NegativeLookahead')
    def _negative_lookahead_(self):
        self._token('!')
        self._cut()
        self._term_()
        self.name_last_node('@')

    @tatsumasu('SkipTo')
    def _skip_to_(self):
        self._token('->')
        self._cut()
        self._term_()
        self.name_last_node('@')

    @tatsumasu()
    def _atom_(self):
        with self._choice():
            with self._option():
                self._cut_()
            with self._option():
                self._cut_deprecated_()
            with self._option():
                self._token_()
            with self._option():
                self._alert_()
            with self._option():
                self._constant_()
            with self._option():
                self._call_()
            with self._option():
                self._pattern_()
            with self._option():
                self._eof_()
            self._error(
                'expecting one of: '
                "'$' '>>' '`' '~' <alert> <call>"
                '<constant> <cut> <cut_deprecated> <eof>'
                '<pattern> <raw_string> <regexes>'
                '<string> <token> <word> \\^+'  # noqa: COM812
            )

    @tatsumasu('RuleRef')
    def _call_(self):
        self._word_()

    @tatsumasu('Void')
    def _void_(self):
        self._token('()')
        self._cut()

    @tatsumasu('Cut')
    def _cut_(self):
        self._token('~')
        self._cut()

    @tatsumasu('Cut')
    def _cut_deprecated_(self):
        self._token('>>')
        self._cut()

    @tatsumasu()
    def _known_name_(self):
        self._name_()
        self._cut()

    @tatsumasu()
    def _name_(self):
        self._word_()

    @tatsumasu('Constant')
    def _constant_(self):
        with self._if():
            self._token('`')
        with self._group():
            with self._choice():
                with self._option():
                    self._pattern('(?ms)```((?:.|\\n)*?)```')
                with self._option():
                    self._token('`')
                    self._literal_()
                    self.name_last_node('@')
                    self._token('`')
                with self._option():
                    self._pattern('`(.*?)`')
                self._error(
                    'expecting one of: '
                    "'`' (?ms)```((?:.|\\n)*?)``` `(.*?)`"  # noqa: COM812
                )

    @tatsumasu('Alert')
    def _alert_(self):
        self._pattern('\\^+')
        self.name_last_node('level')
        self._constant_()
        self.name_last_node('message')

        self._define(
            ['level', 'message'],
            [],
        )

    @tatsumasu('Token')
    def _token_(self):
        with self._choice():
            with self._option():
                self._string_()
            with self._option():
                self._raw_string_()
            self._error(
                'expecting one of: '
                '<STRING> <raw_string> <string> r'  # noqa: COM812
            )

    @tatsumasu()
    def _literal_(self):
        with self._choice():
            with self._option():
                self._string_()
            with self._option():
                self._raw_string_()
            with self._option():
                self._boolean_()
            with self._option():
                self._word_()
            with self._option():
                self._hex_()
            with self._option():
                self._float_()
            with self._option():
                self._int_()
            with self._option():
                self._null_()
            self._error(
                'expecting one of: '
                "'False' 'None' 'True' (?!\\d)\\w+"
                '0[xX](?:\\d|[a-fA-F])+ <STRING> <boolean>'
                '<float> <hex> <int> <null> <raw_string>'
                '<string> <word> [-'
                '+]?(?:\\d+\\.\\d*|\\d*\\.\\d+)(?:[Ee][-'
                '+]?\\d+)? [-+]?\\d+ r'  # noqa: COM812
            )

    @tatsumasu()
    def _string_(self):
        self._STRING_()

    @tatsumasu()
    def _raw_string_(self):
        self._pattern('r')
        self._STRING_()
        self.name_last_node('@')

    @tatsumasu()
    def _STRING_(self):
        with self._choice():
            with self._option():
                self._pattern('"((?:[^"\\n]|\\\\"|\\\\\\\\)*?)"')
                self.name_last_node('@')
                self._cut()
            with self._option():
                self._pattern("'((?:[^'\\n]|\\\\'|\\\\\\\\)*?)'")
                self.name_last_node('@')
                self._cut()
            self._error(
                'expecting one of: '
                '"((?:[^"\\n]|\\"|\\\\)*?)"'
                "'((?:[^'\\n]|\\'|\\\\)*?)'"  # noqa: COM812
            )

    @tatsumasu()
    def _hex_(self):
        self._pattern('0[xX](?:\\d|[a-fA-F])+')

    @tatsumasu()
    def _float_(self):
        self._pattern('[-+]?(?:\\d+\\.\\d*|\\d*\\.\\d+)(?:[Ee][-+]?\\d+)?')

    @tatsumasu()
    def _int_(self):
        self._pattern('[-+]?\\d+')

    @tatsumasu()
    def _path_(self):
        self._pattern('(?!\\d)\\w+(?:::(?!\\d)\\w+)+')

    @tatsumasu()
    def _word_(self):
        self._pattern('(?!\\d)\\w+')

    @tatsumasu('Any')
    def _any_(self):
        self._token('/./')

    @tatsumasu('Pattern')
    def _pattern_(self):
        self._regexes_()

    @tatsumasu()
    def _regexes_(self):

        def sep0():
            self._token('+')

        def block0():
            self._regex_()
        self._positive_gather(block0, sep0)

    @tatsumasu()
    def _regex_(self):
        with self._choice():
            with self._option():
                self._token('/')
                self._cut()
                self._pattern('(?:[^/\\\\]|\\\\/|\\\\.)*')
                self.name_last_node('@')
                self._token('/')
                self._cut()
            with self._option():
                self._token('?/')
                self._cut()
                self._pattern('(?:.|\\n)*?(?=/\\?)')
                self.name_last_node('@')
                self._pattern('/\\?+')
                self._cut()
            with self._option():
                self._token('?')
                self._STRING_()
                self.name_last_node('@')
            self._error(
                'expecting one of: '
                "'/' '?' '?/'"  # noqa: COM812
            )

    @tatsumasu()
    def _boolean_(self):
        with self._choice():
            with self._option():
                self._token('True')
            with self._option():
                self._token('False')
            self._error(
                'expecting one of: '
                "'False' 'True'"  # noqa: COM812
            )

    @tatsumasu()
    def _null_(self):
        self._token('None')

    @tatsumasu('EOF')
    def _eof_(self):
        self._token('$')
        self._cut()


class EBNFBootstrapSemantics:
    def start(self, ast):
        return ast

    def grammar(self, ast):
        return ast

    def directive(self, ast):
        return ast

    def keywords(self, ast):
        return ast

    def keyword(self, ast):
        return ast

    def paramdef(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def decorator(self, ast):
        return ast

    def params(self, ast):
        return ast

    def first_param(self, ast):
        return ast

    def kwparams(self, ast):
        return ast

    def pair(self, ast):
        return ast

    def expre(self, ast):
        return ast

    def choice(self, ast):
        return ast

    def option(self, ast):
        return ast

    def sequence(self, ast):
        return ast

    def element(self, ast):
        return ast

    def rule_include(self, ast):
        return ast

    def named(self, ast):
        return ast

    def named_list(self, ast):
        return ast

    def named_single(self, ast):
        return ast

    def override(self, ast):
        return ast

    def override_list(self, ast):
        return ast

    def override_single(self, ast):
        return ast

    def override_single_deprecated(self, ast):
        return ast

    def term(self, ast):
        return ast

    def group(self, ast):
        return ast

    def gather(self, ast):
        return ast

    def positive_gather(self, ast):
        return ast

    def normal_gather(self, ast):
        return ast

    def join(self, ast):
        return ast

    def positive_join(self, ast):
        return ast

    def normal_join(self, ast):
        return ast

    def left_join(self, ast):
        return ast

    def right_join(self, ast):
        return ast

    def separator(self, ast):
        return ast

    def positive_closure(self, ast):
        return ast

    def closure(self, ast):
        return ast

    def empty_closure(self, ast):
        return ast

    def optional(self, ast):
        return ast

    def special(self, ast):
        return ast

    def lookahead(self, ast):
        return ast

    def negative_lookahead(self, ast):
        return ast

    def skip_to(self, ast):
        return ast

    def atom(self, ast):
        return ast

    def call(self, ast):
        return ast

    def void(self, ast):
        return ast

    def cut(self, ast):
        return ast

    def cut_deprecated(self, ast):
        return ast

    def known_name(self, ast):
        return ast

    def name(self, ast):
        return ast

    def constant(self, ast):
        return ast

    def alert(self, ast):
        return ast

    def token(self, ast):
        return ast

    def literal(self, ast):
        return ast

    def string(self, ast):
        return ast

    def raw_string(self, ast):
        return ast

    def STRING(self, ast):
        return ast

    def hex(self, ast):
        return ast

    def float(self, ast):
        return ast

    def int(self, ast):
        return ast

    def path(self, ast):
        return ast

    def word(self, ast):
        return ast

    def any(self, ast):
        return ast

    def pattern(self, ast):
        return ast

    def regexes(self, ast):
        return ast

    def regex(self, ast):
        return ast

    def boolean(self, ast):
        return ast

    def null(self, ast):
        return ast

    def eof(self, ast):
        return ast


def main(filename, **kwargs):
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        text = Path(filename).read_text()
    parser = EBNFBootstrapParser()
    return parser.parse(
        text,
        filename=filename,
        **kwargs,
    )


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, EBNFBootstrapParser, name='EBNFBootstrap')
    data = asjson(ast)
    print(json.dumps(data, indent=2))

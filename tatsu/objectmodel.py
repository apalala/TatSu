from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from functools import cache

from tatsu.util import asjson, asjsons
from tatsu.infos import CommentInfo
from tatsu.ast import AST
# TODO: from tatsu.exceptions import NoParseInfo


BASE_CLASS_TOKEN = '::'


class Node(object):
    def __init__(self, ctx=None, ast=None, parseinfo=None, **kwargs):
        super().__init__()
        self._ctx = ctx
        self._ast = ast

        if isinstance(ast, AST):
            parseinfo = ast.parseinfo if not parseinfo else None
        self._parseinfo = parseinfo

        attributes = ast if ast is not None else {}
        # assume that kwargs contains node attributes of interest
        if isinstance(attributes, MutableMapping):
            attributes.update(kwargs)

        self.__postinit__(attributes)

    def __postinit__(self, ast):
        if not isinstance(ast, Mapping):
            return

        for name in set(ast) - {'parseinfo'}:
            try:
                setattr(self, name, ast[name])
            except AttributeError:
                raise AttributeError("'%s' is a reserved name" % name)

    @property
    def ast(self):
        return self._ast

    @property
    def line(self):
        if self.parseinfo:
            return self.parseinfo.line

    @property
    def endline(self):
        if self.parseinfo:
            return self.parseinfo.endline

    def text_lines(self):
        return self.parseinfo.text_lines()

    def line_index(self):
        return self.parseinfo.line_index()

    @property
    def col(self):
        return self.line_info.col if self.line_info else None

    @property
    def ctx(self):
        return self._ctx

    @property
    def context(self):
        return self._ctx

    def has_parseinfo(self):
        return self._parseinfo is not None

    @property
    def parseinfo(self):
        # TODO:
        # if self._parseinfo is None:
        #     raise NoParseInfo(type(self).__name__)

        return self._parseinfo

    @property
    def line_info(self):
        if self.parseinfo:
            return self.parseinfo.tokenizer.line_info(self.parseinfo.pos)

    @property
    def text(self):
        if not self.parseinfo:
            return ''
        text = self.parseinfo.tokenizer.text
        return text[self.parseinfo.pos:self.parseinfo.endpos]

    @property
    def comments(self):
        if self.parseinfo:
            return self.parseinfo.tokenizer.comments(self.parseinfo.pos)
        return CommentInfo([], [])

    @property
    def children(self):
        return self.children_list()

    def _children(self):
        for child in self._pubdict().values():
            if isinstance(child, Node):
                yield child
            elif isinstance(child, Mapping):
                yield from (c for c in child.values() if isinstance(c, Node))
            elif isinstance(child, (list, tuple)):
                yield from (c for c in child if isinstance(c, Node))

    @cache
    def children_list(self):
        return list(self._children())

    @cache
    def children_set(self):
        return set(self.children_list())

    def asjson(self):
        return asjson(self)

    def _pubdict(self):
        return {
            k: v
            for k, v in vars(self).items()
            if not k.startswith('_')
        }

    def __json__(self):
        return asjson({
            '__class__': type(self).__name__,
            **self._pubdict()
        })

    def __str__(self):
        return asjsons(self)

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


ParseModel = Node

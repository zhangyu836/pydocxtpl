# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from six import text_type
from jinja2 import Environment, nodes
from jinja2.ext import Extension
from jinja2.exceptions import TemplateSyntaxError

from .text import RunX, Segment

class Env(Environment):

    def handle_exception(self, *args, **kwargs):
        exc_type, exc_value, tb = sys.exc_info()
        red_fmt = '\033[31m%s\033[0m'
        blue_fmt = '\033[34m%s\033[0m'
        error_type = red_fmt % ('error type:  %s' % exc_type)
        error_message = red_fmt % ('error message:  %s' % exc_value)
        print(error_type)
        print(error_message)
        if exc_type is TemplateSyntaxError:
            lineno = exc_value.lineno
            source = kwargs['source']
            src_lines = source.splitlines()
            for i, line in enumerate(src_lines):
                if i + 1 == lineno:
                    line_str = red_fmt % ('line %d : %s' % (i + 1, line))
                elif i + 1 in [lineno - 1, lineno + 1]:
                    line_str = blue_fmt % ('line %d : %s' % (i + 1, line))
                else:
                    line_str = 'line %d : %s' % (i + 1, line)
                print(line_str)
        Environment.handle_exception(self, *args, **kwargs)

class NodeExtension(Extension):
    tags = set(['node', 'root', 'body', 'para', 'run', 'hyperlink',
                'table', 'row', 'cell', 'default', 'headtail'])

    def __init__(self, environment):
        super(self.__class__, self).__init__(environment)
        environment.extend(root = None)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = []
        return nodes.CallBlock(self.call_method('_node', args),
                               [], [], body).set_lineno(lineno)

    def _node(self, key, caller):
        node = self.environment.root.get_node(key)
        return key

class SegmentExtension(Extension):
    tags = set(['seg'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endseg'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_seg', args),
                               [], [], body).set_lineno(lineno)

    def _seg(self, key, caller):
        node = self.environment.root.get_node(key)
        rv = caller()
        rv = node.process_rv(rv)
        return rv

class PicExtension(Extension):
    tags = set(['pic', 'img'])

    def __init__(self, environment):
        super(self.__class__, self).__init__(environment)
        environment.extend(root = None)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = []
        return nodes.CallBlock(self.call_method('_node', args),
                               [], [], body).set_lineno(lineno)

    def _node(self, fname, caller):
        node = self.environment.root.current_node
        fname = text_type(fname)
        if isinstance(node, RunX):
            node._parent.replace_pic(fname)
        elif isinstance(node, Segment):
            node._parent._parent.replace_pic(fname)
        return fname
# -*- coding: utf-8 -*-

from __future__ import print_function
from docx import Document
from .node import Root
from .ext import Env, NodeExtension, SegmentExtension, PicExtension

class DocxWriter(object):

    def __init__(self, fname, debug=False):
        self.debug = debug
        self.load(fname)

    def load(self, fname):
        self.document = Document(fname)
        self.root = Root(self.document)
        self.prepare_env()
        self.tpl_source = self.root.to_tag()
        if self.debug:
            self.root.tag_tree()
            print(self.tpl_source)
        self.jinja_tpl = self.jinja_env.from_string(self.tpl_source)
        self.jinja_env.root = self.root

    def prepare_env(self):
        self.jinja_env = Env(extensions=[NodeExtension, SegmentExtension, PicExtension])

    def render(self, payload):
        rv = self.jinja_tpl.render(payload)

    def save(self, fname):
        self.document.save(fname)
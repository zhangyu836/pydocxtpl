# -*- coding: utf-8 -*-

from __future__ import print_function
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from .node import Root
from .ext import Env, NodeExtension, SegmentExtension, PicExtension

class DocxWriter(object):

    reltypes = [RT.HEADER, RT.FOOTER]

    def __init__(self, fname, debug=False):
        self.debug = debug
        self.load(fname)

    def load(self, fname):
        self.prepare_env()
        self.tpls = []
        self.roots = []
        self.document = Document(fname)
        for rel in self.document.part.rels.values():
            if rel.reltype in self.reltypes:
                root = Root(rel._target)
                if root.unpacked:
                    self.roots.append(root)
        root = Root(self.document)
        if root.unpacked:
            self.roots.append(root)
        for root in self.roots:
            tpl_source = root.to_tag()
            if self.debug:
                root.tag_tree()
                print(tpl_source)
            jinja_tpl = self.jinja_env.from_string(tpl_source)
            self.tpls.append((root, jinja_tpl, tpl_source))

    def prepare_env(self):
        self.jinja_env = Env(extensions=[NodeExtension, SegmentExtension, PicExtension])

    def render(self, payload):
        for root,jinja_tpl,tpl_source in self.tpls:
            self.jinja_env.root = root
            rv = jinja_tpl.render(payload)

    def save(self, fname):
        self.document.save(fname)
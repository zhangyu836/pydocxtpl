# -*- coding: utf-8 -*-

from __future__ import print_function
from docx.oxml import CT_P, CT_R
from docx.oxml.xmlchemy import BaseOxmlElement, ZeroOrOne, ZeroOrMore, OneAndOnlyOne

class CT_Drawing(BaseOxmlElement):
    inline = OneAndOnlyOne('wp:inline')

class CT_Run(CT_R):
    drawing = ZeroOrOne('w:drawing')

class CT_Hyperlink(BaseOxmlElement):
    r = ZeroOrMore('w:r')

class CT_Para(CT_P):
    hyperlink = ZeroOrMore('w:hyperlink')

from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.shared import Parented

from .node import RvNode
from .utils import control_split, var_split, tag_test, fix_test, tag_fix

class ParagraghX(Paragraph, RvNode):
    ext_tag = 'para'

    def __init__(self, element, parent):
        Paragraph.__init__(self, element, parent)
        RvNode.__init__(self)
        self.unpack_p()
        self.current_drawing = None

    def unpack_p(self):
        if not tag_test(self.text + self.hyperlink_text):
            return
        self.fix_and_unpack()

    def fix_and_unpack(self):
        text_4_fix = self.text_4_fix()
        if fix_test(text_4_fix):
            fixed = tag_fix(text_4_fix)
            #print(text_4_fix)
            #print(fixed)
            for i, sub_element in enumerate(self._element):
                if i in fixed:
                    text = fixed[i]
                    if text == '':
                        if sub_element.text != '':
                            continue
                        #else:#drawing
                    else:
                        sub_element.text = text
                node_cls = self.get_node_cls(sub_element)
                child = node_cls(sub_element, self)
                self.add_child(child)
            self.clear_element()
        else:
            RvNode.unpack_and_clear(self)
        self.unpacked = True

    def register_drawing(self, drawing):
        self.current_drawing = drawing

    def replace_pic(self, fname):
        if self.current_drawing is None:
            return
        try:
            rId, image = self.part.get_or_add_image(fname)
        except:
            return
        inline = self.current_drawing.inline
        inline.docPr.id = self.part.next_id
        inline.docPr.name = fname
        inline.docPr.descr = fname
        pic = inline.graphic.graphicData.pic
        pic.nvPicPr.cNvPr.id = 0#pic_id
        pic.nvPicPr.cNvPr.name = fname
        pic.blipFill.blip.embed = rId

    @property
    def print_tag(self):
        return self.node_tag + '  ' + self.text

    @property
    def hyperlinks(self):
        return [Hyperlink(hyperlink, self) for hyperlink in self._p.hyperlink_lst]

    @property
    def hyperlink_text(self):
        text = ''
        for hyperlink in self.hyperlinks:
            text += hyperlink.text
        return text

    def text_4_fix(self):
        text = ''
        tmpl = '___%d___'
        for i,elm in enumerate(self._element):
            if isinstance(elm, CT_R):
                text += (tmpl % i ) + elm.text
        return text


class RunX(Run, RvNode):
    ext_tag = 'run'

    def __init__(self, element, parent):
        Run.__init__(self, element, parent)
        RvNode.__init__(self)
        self.unpack_r()

    def unpack_r(self):
        if not tag_test(self.text):
            return
        parts = control_split(self.text)
        for index,part in enumerate(parts):
            if part == '':
                continue
            if index % 2 == 0:
                sub_parts = var_split(part)
                for sub_index, sub_part in enumerate(sub_parts):
                    if sub_part == '':
                        continue
                    if sub_index % 2 == 0:
                        child = TextSegment(sub_part, self)
                    else:
                        child = VarSegment(sub_part, self)
                    self.add_child(child)
            else:
                child = ControlSegment(part, self)
                self.add_child(child)
        self.unpacked = True

    def enter(self):
        self.rv = self.copy_element()
        if self.rv.drawing is not None:
            self._parent.register_drawing(self.rv.drawing)
        self.children_rvs = ''

    def process_child_rv(self, rv):
        self.children_rvs += rv

    def exit(self):
        if self._children:
            self.rv.text = self.children_rvs
        self._parent.process_child_rv(self.rv)

    @property
    def print_tag(self):
        return self.node_tag + '  ' + self.text

class Segment(RvNode):

    def __init__(self, text, parent):
        RvNode.__init__(self)
        self.text = text
        self._parent = parent

    def process_rv(self, rv):
        self.rv = rv
        return rv

    def enter(self):
        self.rv = ''

class TextSegment(Segment):

    @property
    def node_tag(self):
        tmpl = "{%%seg '%s'%%}{%%endseg%%}"
        return tmpl % self.node_key

    def process_rv(self, rv):
        self.rv = self.text
        return self.text

class VarSegment(Segment):

    @property
    def node_tag(self):
        tmpl = "{%%seg '%s'%%}%s{%%endseg%%}"
        return tmpl % (self.node_key, self.text)

class ControlSegment(Segment):

    @property
    def node_tag(self):
        tmpl = "%s{%%seg '%s'%%}{%%endseg%%}"
        return tmpl % (self.text, self.node_key)


class Hyperlink(Parented):

    def __init__(self, hyperlink, parent):
        super(Hyperlink, self).__init__(parent)
        self._hyperlink = self._element = hyperlink

    def add_run(self, text=None, style=None):
        r = self._hyperlink.add_r()
        run = Run(r, self)
        if text:
            run.text = text
        if style:
            run.style = style
        return run

    def clear(self):
        self._hyperlink.clear_content()
        return self

    @property
    def runs(self):
        return [Run(r, self) for r in self._hyperlink.r_lst]

    @property
    def text(self):
        text = ''
        for run in self.runs:
            text += run.text
        return text

    @text.setter
    def text(self, text):
        self.clear()
        self.add_run(text)

class HyperlinkX(Hyperlink, RvNode):
    ext_tag = 'hyperlink'

    def __init__(self, hyperlink, parent):
        Hyperlink.__init__(self, hyperlink, parent)
        RvNode.__init__(self)
        self.unpack_hyperlink()
        self.current_drawing = None

    def unpack_hyperlink(self):
        if not tag_test(self.text):
            return
        self.fix_and_unpack()

    fix_and_unpack = ParagraghX.fix_and_unpack
    text_4_fix = ParagraghX.text_4_fix
    register_drawing = ParagraghX.register_drawing
    replace_pic = ParagraghX.replace_pic

    @property
    def print_tag(self):
        return self.node_tag + '   ' + self.text

# -*- coding: utf-8 -*-

from docx.table import Table, _Row, _Cell
from .node import RvNode

class TableX(Table, RvNode):
    ext_tag = 'table'

    def __init__(self, element, parent):
        Table.__init__(self, element, parent)
        RvNode.__init__(self)
        self.unpack_table()

    def unpack_table(self):
        self.unpack_and_clear()

class RowX(_Row, RvNode):
    ext_tag = 'row'

    def __init__(self, element, parent):
        _Row.__init__(self, element, parent)
        RvNode.__init__(self)
        self.unpack_row()

    def unpack_row(self):
        self.unpack_and_clear()

    def child_reenter(self):
        self.exit()
        self.enter()

class CellX(_Cell, RvNode):
    ext_tag = 'cell'

    def __init__(self, element, parent):
        _Cell.__init__(self, element, parent)
        RvNode.__init__(self)
        self.unpack_cell()

    def unpack_cell(self):
        self.unpack_and_clear()

class Range(object):
    pass


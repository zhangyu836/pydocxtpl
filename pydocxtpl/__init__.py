# -*- coding: utf-8 -*-

from docx.oxml import CT_Body, CT_Tbl, CT_Row, CT_Tc, CT_R
from docx.oxml import register_element_cls

from .node import BodyX, node_clses
from .text import ParagraghX, RunX, HyperlinkX
from .text import CT_Para, CT_Run, CT_Hyperlink, CT_Drawing
from .table import TableX, RowX, CellX

register_element_cls('w:p', CT_Para)
register_element_cls('w:hyperlink', CT_Hyperlink)
register_element_cls('w:r', CT_Run)
register_element_cls('w:drawing', CT_Drawing)

def register_node_cls(xml_cls, cls):
    node_clses[xml_cls] = cls

register_node_cls(CT_Body, BodyX)
register_node_cls(CT_Para, ParagraghX)
register_node_cls(CT_Run, RunX)
register_node_cls(CT_Tbl, TableX)
register_node_cls(CT_Row, RowX)
register_node_cls(CT_Tc, CellX)
register_node_cls(CT_Hyperlink, HyperlinkX)

from .writer import DocxWriter

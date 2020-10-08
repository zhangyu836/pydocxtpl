# -*- coding: utf-8 -*-

from __future__ import print_function
from copy import deepcopy
from docx.document import _Body
from .utils import TreeProperty

node_clses = {}
class Node(object):
    node_map = TreeProperty('node_map')
    ext_tag = 'node'

    def __init__(self):
        self._children = []

    @property
    def depth(self):
        if not hasattr(self, '_depth'):
            if not hasattr(self, '_parent') or self._parent is self:
                self._depth = 0
            else:
                self._depth = self._parent.depth + 1
        return self._depth

    @property
    def node_key(self):
        return '%s,%s' % (self._parent.node_key, self.no)

    @property
    def node_tag(self):
        return "{%%%s '%s' %%}" % (self.ext_tag, self.node_key)

    @property
    def print_tag(self):
        return self.node_tag

    def children_to_tag(self):
        x = []
        for child in self._children:
            x.append(child.to_tag())
        return '\n'.join(x)

    def to_tag(self):
        self.node_map[self.node_key] = self
        if self._children:
            return self.children_to_tag()
        return self.node_tag

    def tag_tree(self):
        print('\t' * self.depth, self.print_tag)
        for child in self._children:
            child.tag_tree()

    def get_node_cls(self, sub_element):
        return node_clses.get(type(sub_element), Default)

    def unpack_element(self):
        for sub_element in self._element:
            node_cls = self.get_node_cls(sub_element)
            child = node_cls(sub_element, self)
            self.add_child(child)

    def clear_element(self):
        elms = self._element[:]
        for elm in elms:
            self._element.remove(elm)

    def unpack_and_clear(self):
        self.unpack_element()
        self.clear_element()

    def copy_element(self):
        return deepcopy(self._element)

    def add_child(self, child):
        child.no = len(self._children)
        #child._parent = self
        self._children.append(child)

    def enter(self):
        pass

    def reenter(self):
        self.enter()

    def child_reenter(self):
        pass

    def exit(self):
        pass

    def process_child_rv(self, rv):
        pass

    def __str__(self):
        return self.__class__.__name__ +' , ' + self.node_tag

class HtNode(Node):
    ext_tag = 'headtail'

    def __init__(self, parent):
        self._parent = parent
        Node.__init__(self)

    def to_tag(self):
        if self.no == 0:
            return ''
        else:
            return Node.to_tag(self)

class Root(Node):
    ext_tag = 'root'

    def __init__(self, root):
        self._root = root
        self._element = root._element
        self._parent = self
        self.part = root.part
        self.node_map = {}
        Node.__init__(self)
        head_node = HtNode(self)
        tail_node = HtNode(self)
        self.add_child(head_node)
        self.unpack_element()
        self.add_child(tail_node)
        self.current_node = head_node
        self.current_key = ''

    @property
    def node_key(self):
        return '0'

    def find_lca(self, pre, next):
        # find lowest common ancestor
        next_branch = []
        if pre.depth > next.depth:
            for i in range(next.depth, pre.depth):
                pre.exit()
                # print(pre, 'pre up', pre._parent)
                pre = pre._parent

        elif pre.depth < next.depth:
            for i in range(pre.depth, next.depth):
                next_branch.insert(0, next)
                # print(next, 'next up', next._parent)
                next = next._parent
        if pre is next:
            pass
        else:
            pre_parent = pre._parent
            next_parent = next._parent
            while pre_parent != next_parent:
                # print(pre, next, 'up together')
                pre.exit()
                pre = pre_parent
                pre_parent = pre._parent
                next_branch.insert(0, next)
                next = next_parent
                next_parent = next._parent
            pre.exit()
            if pre_parent._children.index(pre) > pre_parent._children.index(next):
                pre_parent.child_reenter()
                next.reenter()
            else:
                next.enter()

        for next in next_branch:
            next.enter()

    def get_node(self, key):
        #if self.current_key == key:
        #    return self.current_node
        self.last_node = self.current_node
        self.last_key = self.current_key
        self.current_node = self.node_map.get(key)
        self.current_key = key
        self.find_lca(self.last_node, self.current_node)
        return self.current_node

class RvNode(Node):
    ext_tag = 'rv'

    def enter(self):
        self.rv = self.copy_element()

    def exit(self):
        self._parent.process_child_rv(self.rv)

    def process_child_rv(self, rv):
        self.rv.append(rv)

class BodyX(_Body, RvNode):
    ext_tag= 'body'

    def __init__(self, element, parent):
        _Body.__init__(self, element, parent)
        RvNode.__init__(self)
        self.unpack_element()

    def enter(self):
        self.clear_element()
        self.rv = self._element


class Default(RvNode):
    ext_tag = 'default'

    def __init__(self, element, parent):
        RvNode.__init__(self)
        self._element = element
        self._parent = parent
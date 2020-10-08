# -*- coding: utf-8 -*-
import re

BLOCK_START_STRING = '{%'
BLOCK_END_STRING = '%}'
VARIABLE_START_STRING = '{{'
VARIABLE_END_STRING = '}}'
TAGTEST = '%s.+%s|%s.+%s' % (BLOCK_START_STRING, BLOCK_END_STRING, VARIABLE_START_STRING, VARIABLE_END_STRING)
XVTEST = '^ *%s *xv.+%s *$' % (BLOCK_START_STRING, BLOCK_END_STRING)
BLOCKTEST = '%s.+%s' % (BLOCK_START_STRING, BLOCK_END_STRING)
BLOCKMIX = '({%(?:(?!%}).)+?)(___\d*___)(.+?%})'# % (BLOCK_START_STRING, BLOCK_END_STRING)
CONTROLSPLIT = '((?:%s.+?%s)+)' % (BLOCK_START_STRING, BLOCK_END_STRING)
CONTROLSPLIT2 = '((?:%s(?:(?!yn ).)+?%s)+)' % (BLOCK_START_STRING, BLOCK_END_STRING)
VARSPLIT = '((?:%s.+?%s)+)' % (VARIABLE_START_STRING, VARIABLE_END_STRING)

FIXTEST = '({(?:___\d+___)?(?:{|%).+?(?:}|%)(?:___\d+___)?})'
RUNSPLIT = '(___\d+___)'
RUNSPLIT2 = '___(\d+)___'

def tag_test(txt):
    p = re.compile(TAGTEST)
    rv = p.findall(txt)
    return bool(rv)

def block_tag_test(txt):
    p = re.compile(BLOCKTEST)
    rv = p.findall(txt)
    return bool(rv)

def control_split(txt):
    split_pattern = re.compile(CONTROLSPLIT)
    parts = split_pattern.split(txt)
    return parts

def var_split(txt):
    split_pattern = re.compile(VARSPLIT)
    parts = split_pattern.split(txt)
    return parts

#need a better way to handle this
def fix_test(txt):
    split_pattern = re.compile(FIXTEST)
    parts = split_pattern.split(txt)
    for i, part in enumerate(parts):
        if i % 2 == 1:
            pattern = re.compile(RUNSPLIT)
            rv = pattern.findall(part)
            if rv :
                return True

def tag_fix(txt):
    split_pattern = re.compile(FIXTEST)
    parts = split_pattern.split(txt)
    p = ''
    for i, part in enumerate(parts):
        if i % 2 == 1:
            p += fix_step2(part)
        else:
            p += part
    split_pattern2 = re.compile(RUNSPLIT2)
    parts = split_pattern2.split(p)
    d = {}
    for i in range(1, len(parts), 2):
            d[int(parts[i])] = parts[i + 1]
    return d

def fix_step2(txt):
    split_pattern = re.compile(RUNSPLIT)
    parts = split_pattern.split(txt)
    p0 = ''
    p1 = ''
    for index,part in enumerate(parts):
        if index % 2 == 0:
            p0 += part
        else:
            p1 += part
    return p0+p1

class TreeProperty(object):

    def __init__(self, name):
        self.name = name
        self._name = '_' + name

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value

    def __get__(self, instance, cls):
        if not hasattr(instance, self._name):
            instance.__dict__[self._name] = getattr(instance._parent, self.name)
        return instance.__dict__[self._name]
# -*- coding: utf-8 -*-

import os
def pth(fname):
    pth = os.path.dirname(__file__)
    return os.path.join(pth, fname)

from pydocxtpl import DocxWriter

person_info = {'address': u'福建行中书省福宁州傲龙山庄', 'name': u'龙傲天', 'pic': pth('1.jpg')}
person_info2 = {'address': u'Somewhere over the rainbow', 'name': u'Hello Wizard', 'pic': pth('0.jpg')}
persons = [person_info, person_info2]#
payload = {'persons': persons}

writer = DocxWriter(pth('test.docx'), True)
writer.render(payload)
writer.save(pth('test_result.docx'))

#print(pth('test.docx'), pth('test_result.docx'))








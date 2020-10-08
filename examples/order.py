# -*- coding: utf-8 -*-
'''
Adapted from docxtpl's order.py
'''
import os
def pth(fname):
    pth = os.path.dirname(__file__)
    return os.path.join(pth, fname)

from pydocxtpl import DocxWriter

tpl = DocxWriter(pth('order_tpl.docx'), debug=True)

context = {
    'customer_name': 'Eric',
    'items': [
        {'desc': 'Python interpreters', 'qty': 2, 'price': 'FREE'},
        {'desc': 'Django projects', 'qty': 5403, 'price': 'FREE'},
        {'desc': 'Guido', 'qty': 1, 'price': '100,000,000.00'},
    ],
    'in_europe': True,
    'is_paid': False,
    'company_name': 'The World Wide company',
    'total_price': '100,000,000.00',
}

tpl.render(context)
tpl.save(pth('order_result.docx'))

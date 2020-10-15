
# pydocxtpl
A docx templater. 
 
## How to install

```shell
pip install pydocxtpl
```

## How to use

To use pydocxtpl, you need to be familiar with the [syntax of jinja2 template](https://jinja.palletsprojects.com/). 

*   code sample
```python
from pydocxtpl import DocxWriter

person_info = {'address': u'', 'name': u'', 'pic': '1.jpg'}
person_info2 = {'address': u'Somewhere over the rainbow', 'name': u'Hello Wizard', 'pic': '0.jpg'}
persons = [person_info, person_info2]
payload = {'persons': persons}

writer = DocxWriter('test.docx')
writer.render(payload)
writer.save('test_result.docx')
```

See [examples](https://github.com/zhangyu836/python-docx-templater/tree/main/examples).

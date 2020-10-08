
# pydocxtpl
使用 docx 文件作为模板来生成 docx 文件。 
 
## 安装

```shell
pip install pydocxtpl
```

## 使用

要使用 pydocxtpl，需要了解 [jinja2 模板的语法](http://docs.jinkan.org/docs/jinja2/templates.html) 。  
如果用过 [docxtpl](https://github.com/elapouya/python-docx-template) ，应该就会用 pydocxtpl。 

*   示例代码
```python
from pydocxtpl import DocxWriter

person_info = {'address': u'福建行中书省福宁州傲龙山庄', 'name': u'龙傲天', 'pic': '1.jpg'}
person_info2 = {'address': u'Somewhere over the rainbow', 'name': u'Hello Wizard', 'pic': '0.jpg'}
persons = [person_info, person_info2]
payload = {'persons': persons}

writer = DocxWriter('test.docx')
writer.render(payload)
writer.save('test_result.docx')
```


## 实现方法

pydocxtpl 也是基于 python-docx 和 jinja2。   
不过实现方法和 [docxtpl](https://github.com/elapouya/python-docx-template) 不太一样。  
pydocxtpl 会根据 docx 文件的 xml 树生成一棵包含 jinja2 tag 的树。   
pydocxtpl 会合并叶节点的 tag 来作为 jinja2 模板，使用 xml 树作为要生成的文档的模板。  
渲染模板时，相当于通过 jinja2 选择所需的叶节点，叶节点及其枝干会使用相应的 xml 树节点生成所需的 xml 树。   
这种方法应该也适用于其他文档。
          
*   合并叶节点 tag 得到的 jinja2 模板。  

```jinja2
{%para '0,1,0' %}
{%default '0,1,1,0' %}
{%for  person in persons%}{%seg '0,1,1,1,0'%}{%endseg%}
{%run '0,1,1,2' %}
{%run '0,1,1,3' %}
{%seg '0,1,1,4,0'%}{{person.name}}{%endseg%}
{%run '0,1,1,5' %}
{%seg '0,1,1,6,0,0'%}{{ person.name}}{%endseg%}
{%run '0,1,1,6,1' %}
{%run '0,1,1,7' %}
{%run '0,1,1,8' %}
{%default '0,1,2,0' %}
{%run '0,1,2,1' %}
{%run '0,1,2,2' %}
{%seg '0,1,2,3,0'%}{%endseg%}
{%seg '0,1,2,3,1'%}{{person.address}}{%endseg%}
{%run '0,1,2,4' %}
{%default '0,1,3,0' %}
{%run '0,1,3,1' %}
{%seg '0,1,3,2,0'%}{{person.name}}{%endseg%}
{%pic person.pic%}{%seg '0,1,3,3,0'%}{%endseg%}
{%  endfor%}{%seg '0,1,3,4,0'%}{%endseg%}
{%para '0,1,4' %}
{%default '0,1,5,0' %}
{%default '0,1,5,1' %}
{%default '0,1,5,2,0' %}
{%default '0,1,5,2,1,0' %}
{%default '0,1,5,2,1,1,0' %}
{%for person in persons%}{%seg '0,1,5,2,1,1,1,0'%}{%endseg%}
{%seg '0,1,5,2,1,1,2,0'%}{{person.name}}{%endseg%}
{%default '0,1,5,2,2,0' %}
{%default '0,1,5,2,2,1,0' %}
{%seg '0,1,5,2,2,1,1,0'%}{{person.address}}{%endseg%}
{%default '0,1,5,2,3,0' %}
{%default '0,1,5,2,3,1,0' %}
{%run '0,1,5,2,3,1,1' %}
{% pic person.pic%}{%seg '0,1,5,2,3,1,2,0'%}{%endseg%}
{%endfor%}{%seg '0,1,5,2,3,1,3,0'%}{%endseg%}
{%para '0,1,6' %}
{%default '0,1,7' %}
{%headtail '0,2' %}
```
import os
from io import open
from setuptools import setup

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, "README.md")
with open(README, 'r', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name = 'pydocxtpl',
    version = "0.1",
    author = 'Zhang Yu',
    author_email = 'zhangyu836@gmail.com',
    url = 'https://github.com/zhangyu836/python-docx-templater',
    packages = ['pydocxtpl'],
	install_requires = ['python-docx >= 0.8.10', 'jinja2', 'six'],
    description = ( 'A python module to generate docx files from a docx template' ),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    platforms = ["Any platform "],
    license = 'MIT',
    keywords = ['Word', 'docx', 'template']
)
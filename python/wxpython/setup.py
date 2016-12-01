# !/usr/bin/python
# coding:utf-8

from distutils.core import setup
import py2exe

setup(
    windows = ['login.py'],
    options = {
        "py2exe":
            {"dll_excludes": ["MSVCP90.dll"],
             "compressed"  : 1,
             "optimize"    : 2,
             "ascii"       : 0
             }
    }
)

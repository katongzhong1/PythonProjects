# coding: utf-8

from __future__ import unicode_literals

# 实现了一个类来解析简单的类shell语法，可以用来编写领域特定的语言，或者解析加引号的字符串
import shlex


try:
    compat_str = unicode  # Python 2
except NameError:
    compat_str = str


try:
    args = shlex.split('中文')
    assert (isinstance(args, list) and
            isinstance(args[0], compat_str) and
            args[0] == '中文')
    compat_shlex_split = shlex.split
except (AssertionError, UnicodeEncodeError):
    # 在一些python 2上解决unicode字符串的问题

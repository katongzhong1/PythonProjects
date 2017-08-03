#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import sys


# 获取系统编码方式
def get_filesystem_encoding():
    encoding = sys.getfilesystemencoding()
    return encoding if encoding is not None else 'utf-8'
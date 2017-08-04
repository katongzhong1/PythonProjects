#!/usr/bin/env python
# coding: utf-8

# 为了适应Python 3.x的新的字符串的表示方法，在2.7版本的代码中，可以通过unicode_literals来使用Python 3.x的新的语法
from __future__ import unicode_literals

# ?
__license__ = 'Public Domain'

# 专门用作编码转换
import codecs
# 文件读写
import io
#
import os
#
import random
#
import sys


from options import (
    parseOpts,
)

from utils import (
    std_headers,
)


def _real_main(argv=None):
    # windows 兼容性修复
    if sys.platform == 'win32':
        # https://github.com/rg3/youtube-dl/issues/820
        codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

    parser, opts, args = parseOpts(argv)
    # 设置 User-Agent
    if opts.user_agent is not None:
        std_headers['User-Agent'] = opts.user_agent
    # 设置 referer
    if opts.referer is not None:
        std_headers['Referer'] = opts.referer
    # 设置
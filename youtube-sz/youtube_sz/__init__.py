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
    write_string,
)

from utils import (
    std_headers,
    expand_path,
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
    # 设置 HTTP headers
    if opts.headers is not None:
        for h in opts.headers:
            if ':' not in h:
                parser.error('wrong header formatting, it should be key:value, not "%s"' % h)
            key, value = h.split(':', 1)
            if opts.verbose:
                write_string('[debug] Adding header from command line option %s:%s\n' % (key, value))
            std_headers[key] = value
    # 如果设置了 --dump-user-agent 则输出标识
    if opts.dump_user_agent:
        write_string(std_headers['User-Agent'] + '\n', out=sys.stdout)
        sys.exit(0)
    # 批量文件验证
    batch_urls = []
    if opts.batchfile is not None:
        try:
            if opts.batchfile == '-':
                batchfd = sys.stdin
            else:
                batchfd = io.open(
                    expand_path(opts.batchfile),
                    'r', encoding='utf-8', errors='ignore'
                )
            batch_urls

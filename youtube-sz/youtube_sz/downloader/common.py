#!/usr/bin/env python
# coding: utf-8

from __future__ import division, unicode_literals

import re

class FileDownloader(object):
    """"""
    @staticmethod
    def parse_bytes(bytestr):
        """解析一个字符串，返回字节(b)数量, 类型为整数 e.g. 1.0k ==> 1024b"""
        matchobj = re.match(r'(?i)^(\d+(?:\.\d+)?)([kMGTPEZY]?)$', bytestr)
        if matchobj is None:
            return None
        number = float(matchobj.group(1))
        # 因数
        multiplier = 1024.0 ** 'bkmgtpezy'.index(matchobj.group(2).lower())
        return int(round(number * multiplier))
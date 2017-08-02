# coding: utf-8

# 命令行参数

from __future__ import unicode_literals

# 用于文件的属性获取
import os.path
# 获取命令行参数
import optparse
# 正则表达式模块
import re
#
import sys


# 获取命令行的参数
def parseOpts(overrideArguments=None):
    def _readOptions(filename_bytes, default=[]):
        try:
            optionf = open(filename_bytes)
        except IOError:
            return default  #如果文件不存在, 则默认跳过
        try:
            #
            contents = optionf.read()
            if sys.version_info < (3,):
                # TODO: 这是做了什么处理
                contents = contents.decode()
            res =
        finally:
            optionf.close()
        return res

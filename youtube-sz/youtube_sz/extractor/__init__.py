#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals


# 所有提取器
try:
    from .lazy_extractors import *
    from .lazy_extractors import _ALL_CLASSES
    _LAZY_LOADER = True
except ImportError:
    _LAZY_LOADER = False
    from .extractors import *

    _ALL_CLASSES = [
        klass
        for name, klass in globals().items()
        if name.endswith('IE') and name != 'GenericIE'
    ]
    _ALL_CLASSES.append(GenericIE)


def gen_extractor_classes():
    """支持的提取网站
    顺序很重要, 匹配的第一个提取器就是处理该 URL 的那个
    """
    return _ALL_CLASSES


def gen_extractors():
    """返回每个支持的提取器的实例的列表
    """
    return [klass for klass in gen_extractor_classes()]


def list_extractors(age_limit):
    """返回适合指定年龄的提取器实例列表, 通过提取器 ID 排序
    """
    return sorted(
        filter(lambda ie: ie.is_suitable(age_limit), gen_extractors()),
        key=lambda ie: ie.IE_NAME.lower()
    )





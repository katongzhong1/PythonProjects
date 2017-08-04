#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import sys
import io
import os
import locale

from compat import (
    compat_str,   # 字符串类型
    compat_expanduser,
)

# 默认请求头
std_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-us,en;q=0.5',
}

#
def expand_path(s):
    return os.path.expandvars(compat_expanduser(s))


# 获取系统编码方式
def get_filesystem_encoding():
    encoding = sys.getfilesystemencoding()
    return encoding if encoding is not None else 'utf-8'


# 得到最合适的编码方式
def preferredencoding():
    try:
        pref = locale.getpreferredencoding()
        'TEST'.encode(pref)
    except Exception:
        pref = 'UTF-8'
    return pref


# TODO: 需要更详细的了解
def _write_write_string(s, out):
    """返回 True, 如果字符串已经用指定的方法输出, 否则为 False"""
    import ctypes
    import ctypes.wintypes

    WIN_OUTPUT_IDS = {
        1: -11,
        2: -12,
    }

    try:
        # 此方法返回整数的底层实现使用请求从操作系统的I / O操作的文件描述符
        fileno = out.fileno()
    except AttributeError:
        return False
    except io.UnsupportedOperation:
        return False
    if fileno not in WIN_OUTPUT_IDS:
        return False

    # 怎样在Python中创建一个函数，然后让它变成一个可以被Windows API通过函数指针来调用的函数呢？这得使用ctypes.WINFUNCTYPE来实现，
    # 它可以将Python callable对象转换为一个可以被C调用的函数指针
    GetStdHandle = ctypes.WINFUNCTYPE(
        ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
    )((b'GetStdHandle', ctypes.windll.kernel32))
    h = GetStdHandle(WIN_OUTPUT_IDS[fileno])

    WriteConsoleW = ctypes.WINFUNCTYPE(
        ctypes.wintypes.BOOL, ctypes.wintypes.HANDLE, ctypes.wintypes.LPWSTR,
        ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.wintypes.DWORD),
        ctypes.wintypes.LPVOID
    )((b'WriteConsoleW', ctypes.windll.kernel32))
    written = ctypes.wintypes.DWORD(0)

    GetFileType = ctypes.WINFUNCTYPE(
        ctypes.wintypes.DWORD, ctypes.wintypes.DWORD
    )((b'GetFileType', ctypes.windll.kernel32))
    FILE_TYPE_CHAR = 0x0002
    FILE_TYPE_REMOTE = 0x8000
    GetConsoleMode = ctypes.WINFUNCTYPE(
        ctypes.wintypes.BOOL, ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.wintypes.DWORD)
    )((b'GetConsoleMode', ctypes.windll.kernel32))
    INVALID_HANDLE_VALUE = ctypes.wintypes.DWORD(-1).value

    def not_a_console(handle):
        if handle == INVALID_HANDLE_VALUE or handle is None:
            return True
        return ((GetFileType(handle) & ~FILE_TYPE_REMOTE) != FILE_TYPE_CHAR or
                GetConsoleMode(handle, ctypes.byref(ctypes.wintypes.DWORD())) == 0)

    if not_a_console(h):
        return False

    def next_nonbmp_pos(st):
        try:
            return next(i for i, c in enumerate(st) if ord(c) > 0xffff)
        except StopIteration:
            return len(st)

    while s:
        count = min(next_nonbmp_pos(s), 1024)

        ret = WriteConsoleW(
            h, s, count if count else 2, ctypes.byref(written), None
        )
        if ret == 0:
            raise OSError('Failed to write string')
        if not count:
            assert written.value == 2
            s = s[1:]
        else:
            assert written.value > 0
            s = s[written.value:]
    return True


# 写错误日志
def write_string(s, out=None, encoding=None):
    # sys.stderr 输出
    # ==> mac: <open file '<stderr>', mode 'w' at 0x10a3d81e0>
    if out is None:
        out = sys.stderr  # 用来重定向标准错误信息的, 将输出发送到终端或是 IDE
    # 断言: 判断字符串 s 是否是指定的编码类型
    assert type(s) == compat_str

    if sys.platform == 'win32' and encoding is None and hasattr(out, 'fileno'):
        if _write_write_string(s, out):
            return

    if ('b' in getattr(out, 'mode', '') or sys.version_info[0] < 3):
        byt = s.encode(encoding or preferredencoding(), 'ignore')
        out.write(byt)
    elif hasattr(out, 'buffer'):
        enc = encoding or getattr(out, 'encoding', None) or preferredencoding()
        byt = s.encode(enc, 'ignore')
        out.buffer.write(byt)
    else:
        out.write(s)
    out.flush()


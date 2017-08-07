#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import sys
import io
import os
import locale
# 更优雅的方式实现上下文
import contextlib
import datetime
import re
import operator

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


# 处理 Urls
def read_batch_urls(batch_fd):
    def fix_up(url):
        if not isinstance(url, compat_str):
            url = url.decode('utf-8', 'replace')
        # 如果 url 以 \xef\xbb\xbf 开头则去掉此字符串
        # EF BB BF 是被称为 Byte order mark(BOM)的文件标记, 用来指出这个文件是 UTF-8 编码
        # 了解 字节顺序标记(BOM) https://zh.wikipedia.org/wiki/%E4%BD%8D%E5%85%83%E7%B5%84%E9%A0%86%E5%BA%8F%E8%A8%98%E8%99%9F
        BOM_UTF8 = '\xef\xbb\xbf'
        if url.startswith(BOM_UTF8):
            url = url[len(BOM_UTF8):]
        # strip() 函数参数为空时, 默认删除空白符('\n', '\r', '\t', ' ')
        url = url.strip()
        if url.startswith(('#', ';', ']')):
            return False
        return url

    with contextlib.closing(batch_fd) as fd:
        return [url for url in map(fix_up, fd) if url]


def render_table(header_row, data):
    """渲染行列表，每个值作为一个列表的值"""
    table = [header_row] + data
    max_len = [max(len(compat_str(v)) for v in col) for col in zip(*table)]
    format_str = ' '.join('%-' + compat_str(ml + 1) + 's' for ml in max_len[:-1]) + '%s'
    return '\n'.join(format_str % tuple(row) for row in table)


#=======================================================================================================================
# 日期Date相关

def date_from_str(date_str):
    """从字符串返回一个datetime对象"""
    today = datetime.date.today()
    if date_str in ('now', 'today'):
        return today
    if date_str == 'yesterday':
        return today - datetime.timedelta(days=1)
    match = re.match(r'(now|today)(?P<sign>[+-])(?P<time>\d+)(?P<unit>day|week|month|year)(s)?', date_str)
    if match is not None:
        sign = match.group('sign')
        time = int(match.group('time'))
        if sign == '-':
            time = -time
        unit = match.group('unit')
        if unit == 'month':
            unit = 'day'
            time *= 30
        elif unit == 'year':
            unit = 'day'
            time *= 365
        unit += 'S'
        delta = datetime.timedelta(**{unit: time})
        return today + delta
    return datetime.datetime.strptime(date_str, '%Y%m%d').date()


class DateRange(object):
    """表示两个日期之间的时间间隔"""
    def __init__(self, start=None, end=None):
        # start/end 必须是日期格式的字符串
        if start is not None:
            self.start = date_from_str(start)
        else:
            self.start = datetime.datetime.min.date()
        if end is not None:
            self.end = date_from_str(end)
        else:
            self.end = datetime.datetime.max.date()
        if self.start > self.end:
            raise ValueError('Date range: "%s" , the start date must be before than the end date' % self)

    @classmethod
    def day(cls, day):
        """返回仅包含给定日期的范围"""
        return cls(day, day)

    def __contains__(self, date):
        """判断日期是否在范围内"""
        if not isinstance(date, datetime.date):
            date = date_from_str(date)
        return self.start <= date <= self.end

    def __str__(self):
        return '%s - %s' % (self.start.isoformat(), self.end.isoformat())


#=======================================================================================================================
# 名称模板

DEFAULT_OUTTMPL = '%(title)s-%(id)s.%(ext)s'

#=======================================================================================================================
# 文件大小相关

def look_unit_table(unit_table, s):
    units_re = '|'.join(re.escape(u) for u in unit_table)
    # 取到字符串中的数字和单位
    m = re.match(r'(?P<num>[0-9]+(?:[,.][0-9]*)?)\s*(?P<unit>%s)\b' % units_re, s)
    if not m:
        return None
    # 取到数字, 并用'.'替换字符串中的','字符
    num_str = m.group('num').replace(',', '.')
    # 取到单位代表的因子数
    mult = unit_table[m.group('unit')]
    return int(float(num_str) * mult)


def parse_filesize(s):
    if s is None:
        return None

    # 小写的形式是不正确并且非官方的, 但是同样兼容
    _UNIT_TABLE = {
        'B': 1,
        'b': 1,
        'bytes': 1,
        'KiB': 1024,
        'KB': 1000,
        'kB': 1024,
        'Kb': 1000,
        'kb': 1000,
        'kilobytes': 1000,
        'kibibytes': 1024,
        'MiB': 1024 ** 2,
        'MB': 1000 ** 2,
        'mB': 1024 ** 2,
        'Mb': 1000 ** 2,
        'mb': 1000 ** 2,
        'megabytes': 1000 ** 2,
        'mebibytes': 1024 ** 2,
        'GiB': 1024 ** 3,
        'GB': 1000 ** 3,
        'gB': 1024 ** 3,
        'Gb': 1000 ** 3,
        'gb': 1000 ** 3,
        'gigabytes': 1000 ** 3,
        'gibibytes': 1024 ** 3,
        'TiB': 1024 ** 4,
        'TB': 1000 ** 4,
        'tB': 1024 ** 4,
        'Tb': 1000 ** 4,
        'tb': 1000 ** 4,
        'terabytes': 1000 ** 4,
        'tebibytes': 1024 ** 4,
        'PiB': 1024 ** 5,
        'PB': 1000 ** 5,
        'pB': 1024 ** 5,
        'Pb': 1000 ** 5,
        'pb': 1000 ** 5,
        'petabytes': 1000 ** 5,
        'pebibytes': 1024 ** 5,
        'EiB': 1024 ** 6,
        'EB': 1000 ** 6,
        'eB': 1024 ** 6,
        'Eb': 1000 ** 6,
        'eb': 1000 ** 6,
        'exabytes': 1000 ** 6,
        'exbibytes': 1024 ** 6,
        'ZiB': 1024 ** 7,
        'ZB': 1000 ** 7,
        'zB': 1024 ** 7,
        'Zb': 1000 ** 7,
        'zb': 1000 ** 7,
        'zettabytes': 1000 ** 7,
        'zebibytes': 1024 ** 7,
        'YiB': 1024 ** 8,
        'YB': 1000 ** 8,
        'yB': 1024 ** 8,
        'Yb': 1000 ** 8,
        'yb': 1000 ** 8,
        'yottabytes': 1000 ** 8,
        'yobibytes': 1024 ** 8,
    }
    return look_unit_table(_UNIT_TABLE, s)


def _match_one(filter_part, dct):
    # 比较符号
    COMPARISON_OPERATORS = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '=': operator.eq,
        '!=': operator.ne
    }
    operator_rex = re.compile(r'''(?x)\s*
        (?P<key>[a-z_]+)\s*
        (?P<op>%s)(?P<none_inclusive>\s*\?)?\s*
        (?:
            (?P<intval>[0-9.]+(?:[kKmMgGtTpPeEzZyY]i?[Bb]?)?)|
            (?P<quote>["\'])(?P<quotedstrval>(?:\\.|(?!(?P=quote)|\\).)+?)(?P=quote)|
            (?P<strval>(?![0-9.])[a-z0-9A-Z]*)
        )
        \s*$
        ''' % '|'.join(map(re.escape, COMPARISON_OPERATORS.keys())))
    m = operator_rex.search(filter_part)
    if m:
        op = COMPARISON_OPERATORS[m.group('op')]
        actual_value = dct.get(m.group('key'))
        if (m.group('quotedstrval') is not None or
            m.group('strval') is not None or
            actual_value is not None and m.group('intval') is not None and isinstance(actual_value, compat_str)):
            if m.group('op') not in ('=', '!='):
                raise ValueError('Operator %s does not support string values!' % m.group('op'))
            comparison_value = m.group('quotedstrval') or m.group('strval') or m.group('intval')
            quote = m.group('quote')
            if quote is not None:
                comparison_value = comparison_value.replace(r'\%s' % quote, quote)
        else:
            try:
                comparison_value = int(m.group('intval'))
            except ValueError:
                comparison_value = parse_filesize(m.group('intval'))
                if comparison_value is None:
                    comparison_value = parse_filesize(m.group('intval') + 'B')
                if comparison_value is None:
                    raise ValueError(
                        'Invalid integer value %r in filter part %r' % (m.group('intval'), filter_part)
                    )
        if actual_value is None:
            return m.group('none_inclusive')
        return op(actual_value, comparison_value)

    UNARY_OPERATORS = {
        '': lambda v: v is not None,
        '!': lambda v: v is None,
    }
    operator_rex = re.compile(r'''(?x)\s*
        (?P<op>%s)\s*(?P<key>[a-z_]+)
        \s*$
        ''' % '|'.join(map(re.escape, UNARY_OPERATORS.keys())))
    m = operator_rex.search(filter_part)
    if m:
        op = UNARY_OPERATORS[m.group('op')]
        actual_value = dct.get[m.group('key')]
        return op(actual_value)
    return ValueError('Invalid filter part %r' % filter_part)


def match_str(filter_str, dct):
    """用简单的字符串语法过滤字典, 过滤成功则返回 True"""
    return all(_match_one(filter_part, dct) for filter_part in filter_str.split('&'))


def match_filter_func(filter_str):
    def _match_fun(info_dict):
        if match_str(filter_str, info_dict):
            return None
        else:
            video_title = info_dict.get('title', info_dict.get('id', 'video'))
            return '%s does not pass filter %s, skipping ..' % (video_title, filter_str)
    return _match_fun


#=======================================================================================================================
# 编码相关

def decodeOption(optval):
    if optval is None:
        return optval
    if isinstance(optval, bytes):
        optval = optval.decode(preferredencoding())

    assert isinstance(optval, compat_str)
    return optval
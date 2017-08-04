# coding: utf-8

from __future__ import unicode_literals

# 实现了一个类来解析简单的类shell语法，可以用来编写领域特定的语言，或者解析加引号的字符串
import shlex
import sys
import os
# 高层次的文件操作工具
import shutil
#
import collections
#
import subprocess

# 编码方式
try:
    compat_str = unicode  # Python 2
except NameError:
    compat_str = str

# 分割解析命令行字符串
try:
    args = shlex.split('中文')
    assert (isinstance(args, list) and
            isinstance(args[0], compat_str) and
            args[0] == '中文')
    compat_shlex_split = shlex.split
except (AssertionError, UnicodeEncodeError):
    # 在一些python 2上解决unicode字符串的问题
    def compat_shlex_split(s, comments=False, posix=True):
        if isinstance(s, compat_str):
            s = s.encode('utf-8')
        return list(map(lambda tp: tp.decode('utf-8'), shlex.split(s, comments, posix)))

# os_name TODO: os_name? 是 bug, 还是
compat_os_name = os.name if os.name == 'java' else os.name

# 提供与环境变量方法:
#    获取环境变量: compat_getenv
#    设置环境变量: compat_setenv
#    替换 ~ 路径:  compat_expanduser
if sys.version_info >= (3, 0):
    compat_getenv = os.getenv  # 获取环境变量
    compat_expanduser = os.path.expanduser  # 把 path中包含的 ~ 和 ~user 转换成用户目录


    def compat_setenv(key, value, env=os.environ):
        env[key] = value
else:
    # 应使用文件系统编码对环境变量进行解码
    # 否则，如果存在任何非ASCII字符，它将失败 (see #3854 #3217 #2918)
    def compat_getenv(key, default=None):
        from utils import get_filesystem_encoding
        env = os.getenv(key, default)
        if env:
            env = env.decode(get_filesystem_encoding())
        return env


    def compat_setenv(key, value, env=os.environ):
        def encode(v):
            from utils import get_filesystem_encoding
            return v.encode(get_filesystem_encoding()) if isinstance(v, compat_str) else v

        # 如果是 unicode编码, 则需要使用文件系统编码方式先进行编码, 然后才能设置环境变量
        env[encode(key)] = encode(value)


    # HACK: 来自 cpython 的 os.path.expanduser 默认实现不会用文件系统编码解码环境变量;
    # 我们将通过调整实现来解决这个问题。以下是来自 cpython 2.7.8 的实现, 用于不用平台正确的设置环境变量解码

    if compat_os_name == 'posix':  # 表示 Linux
        def compat_expanduser(path):
            """用具体的路径替代~和~user, 如果用户或者$HOME未知,
            则什么也不做"""
            if not path.startswith('~'):
                return path
            i = path.find('/', 1)
            if i < 0:
                i = len(path)
            if i == 1:
                if 'HOME' not in os.environ:
                    import pwd  # unix用户及用户组
                    # pwd.getpwuid(uid)：返回对应uid的示例信息
                    # >>> pwd.getpwuid(0)
                    # >>> pwd.struct_passwd(pw_name='root', pw_passwd='x', pw_uid=0, pw_gid=0, pw_gecos='root', pw_dir='/root', pw_shell='/bin/bash')
                    userhome = pwd.getpwuid(os.geteuid()).pw_dir
                else:
                    userhome = compat_getenv('HOME')
            else:
                import pwd
                try:
                    # pwd.getpwnam(name)：返回对应name的用户信息
                    pwent = pwd.getpwnam(path[1:i])
                except KeyError:
                    return path
                userhome = pwent.pw_dir
            userhome = userhome.rstrip('/')  # 去除尾部的'/'符号
            return (userhome + path[i:]) or '/'
    elif compat_os_name in ('nt', 'ce'):  # nt 代表 windows
        def compat_expanduser(path):
            if path[:1] != '~':
                return path
            # TODO:这里做了什么
            i, n = 1, len(path)
            while i < n and path[i] not in '/\\':
                i = i + 1

            if 'HOME' in os.environ:
                userhome = compat_getenv('HOME')
            elif 'USERPROFILE' in os.environ:
                userhome = compat_getenv('USERPROFILE')
            elif 'HOMEPATH' not in os.environ:
                return path
            else:
                try:
                    drive = compat_getenv('HOMEDTRIVE')
                except KeyError:
                    drive = ''
                userhome = os.path.join(drive, compat_getenv('HOMEDRIVE'))

            if i != 1:  # ~user
                userhome = os.path.join(os.path.dirname(userhome), path[1:i])

            return userhome + path[i:]
    else:
        compat_expanduser = os.path.expanduser

# 获取命令行的大小
if hasattr(shutil, 'get_terminal_size'):  # Python >= 3.3
    compat_get_terminal_size = shutil.get_terminal_size
else:
    # namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。
    _terminal_size = collections.namedtuple('terminal_size', ['columns', 'lines'])


    def compat_get_terminal_size(fallback=(80, 24)):
        columns = compat_getenv('COLUMNS')
        if columns:
            columns = int(columns)
        else:
            columns = None
        lines = compat_getenv('LINES')
        if lines:
            lines = int(lines)
        else:
            lines = None

        if columns is None or lines is None or columns <= 0 or lines <= 0:
            try:
                # 生成子线程, 执行指令, 并获取执行结果
                sp = subprocess.Popen(
                    ['stty', 'size'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                # communicate()是Popen对象的一个方法，该方法会阻塞父进程，直到子进程完成
                out, err = sp.communicate()
                _lines, _columns = map(int, out.split())
            except Exception:
                _columns, _lines = _terminal_size(*fallback)

            if columns is None or columns <= 0:
                columns = _columns
            if lines is None or lines <= 0:
                lines = _lines
        return _terminal_size(columns, lines)


# Python <2.6.5要求kwargs是字节
try:
    def _testfunc(x):
        pass
    _testfunc(**{'x': 0})
except TypeError:
    def compat_kwargs(kwargs):
        return dict((bytes(k), v) for k, v in kwargs.items())
else:
    compat_kwargs = lambda kwargs: kwargs

__all__ = [
    'compat_shlex_split',  # 分解命令行的参数
    'compat_getenv',  # 获取指定key的环境变量
    'compat_expanduser',  # 获取全路径, 主要是替换路径中~和~user
    'compat_setenv',  # 设置环境变量
    'compat_get_terminal_size',  # 获取控制台(命令行)大小
    'compat_kwargs',  # 兼容 python低版本, 参数的 key 值需为字节
]

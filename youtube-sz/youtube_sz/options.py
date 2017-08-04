# coding: utf-8

# 返回 parse, opts, args

from __future__ import unicode_literals

# 用于文件的属性获取
import os.path
# 获取命令行参数
import optparse
# 正则表达式模块
import re
#
import sys

from compat import (
    # 分解命令行的参数
    compat_shlex_split,
    # 获取指定key的环境变量
    compat_getenv,
    # 获取全路径, 主要是替换路径中~和~user
    compat_expanduser,
    # 获取终端大小(columns, lines)
    compat_get_terminal_size,
    compat_kwargs,
)

from utils import (
    write_string,
    # 获取编码方式
    preferredencoding,
)

from verison import __version__


# 隐藏登录相关的信息
def _hide_login_info(opts):
    PRIVATE_OPTS = {'-p', '--password', '-u', '--username', '--video-password', '--ap-password', '--ap-username'}
    eqre = re.compile('^(?P<key>' + ('|'.join(re.escape(po) for po in PRIVATE_OPTS)) + ')=.+$')

    def _scrub_eq(o):
        m = eqre.match(o)
        if m:
            return m.group('key') + '=PRIVATE'
        else:
            return o

    opts = list(map(_scrub_eq, opts))
    for idx, opt in enumerate(opts):
        if opt in PRIVATE_OPTS and idx + 1 < len(opts):
            opts[idx + 1] = 'PRIVATE'
    return opts


# 获取命令行的参数
def parseOpts(overrideArguments=None):
    """读取指定路径的文件, 返回内容, 返回格式为 list
    """
    def _readOptions(filename_bytes, default=[]):
        try:
            optionf = open(filename_bytes)
        except IOError:
            # 如果文件不存在, 则默认跳过
            return default
        try:
            #
            contents = optionf.read()
            if sys.version_info < (3,):
                # TODO: 判断 python 版本小于3, 则需要先解码？
                contents = contents.decode()
            res = compat_shlex_split(contents, comments=True)
        finally:
            optionf.close()
        return res

    """读取用户配置文件"""
    def _readUserConf():
        xdg_config_home = compat_getenv('XDG_CONFIG_HOME')
        if xdg_config_home:
            userConfFile = os.path.join(xdg_config_home, 'youtube-dl', 'config')
            if not os.path.isfile(userConfFile):
                userConfFile = os.path.join(xdg_config_home, 'youtube-dl.conf')
        else:
            userConfFile = os.path.join(compat_expanduser('~'), '.config', 'youtube-dl', 'config')
            if not os.path.isfile(userConfFile):
                userConfFile = os.path.join(compat_expanduser('~'), '.config', 'youtube-dl.conf')
        userConf = _readOptions(userConfFile)

        if userConf is None:
            appdata_dir = compat_getenv('appdata')
            if appdata_dir:
                userConf = _readOptions(os.path.join(appdata_dir, 'youtube-dl', 'config'))
                if userConf is None:
                    userConf = _readOptions(os.path.join(appdata_dir, 'youtube-dl', 'config.txt'))

        if userConf is None:
            userConf = _readOptions(
                os.path.join(compat_expanduser('~'), 'youtube-dl.conf'),
            )
        if userConf is None:
            userConf = _readOptions(
                os.path.join(compat_expanduser('~'), 'youtube-dl.conf.txt'),
            )

        if userConf is None:
            userConf = []

        return userConf

    # 格式化参数字符串  option 是什么类型
    def _format_option_string(option):
        # ('-o', '--option') -> -o, --format METAVAR
        """

        :type option: Option
        """
        opts = []

        if option._short_opts:
            opts.append(option._short_opts[0])
        if option._long_opts:
            opts.append(option._long_opts[0])
        if len(opts) > 1:
            opts.insert(1, ', ')

        if option.takes_value():
            opts.append(' %s' % option.metavar)

        return ''.join(opts)

    def _comma_separated_values_options_callback(option, opt_str, value, parser):
        """setattr(object, name, values)
           给对象的属性赋值，若属性不存在，先创建再赋值。
        """
        setattr(parser.values, option.dest, value.split(','))

    # 程序入口
    # 如果是在控制台上, 不需要显示帮助信息
    columns = compat_get_terminal_size().columns
    max_width = columns if columns else 80
    max_help_position = 80

    fmt = optparse.IndentedHelpFormatter(width=max_width, max_help_position=max_help_position)
    fmt.format_option_strings = _format_option_string

    kw = {
        'version': __version__,
        'formatter': fmt,
        'usage': '%prog [OPTIONS] URL [URL...]',
        'conflict_handler': 'resolve',
    }
    # 创建一个命令行选项解析器 kw中的值都代表着 OptionParser 的参数
    # 由此可以看出多参, 如何用 dict 传参
    """
    (1).prog:当前脚本程序的名称;os.path.basename(sys.argv[0]);
    (2).usage:描述当前脚本程序的用法字符串;显示该用法之前,格式"%prog"将被格式化成当前脚本程序的名称;
    (3).description:当前脚本程序的简单描述、摘要、大纲;它会被显示在命令行选项的帮助之前;
    (4).epilog:当前脚本程序的简单描述、摘要、大纲;它会被它会被显示在命令行选项的帮助之后;
    (5).conflict_handler:命令行选项冲突处理器;比如,当命令行选项重复时,该如何让处理;可选值:error、resolve;
    (6).add_help_option:是否自动生成帮助信息;True:是; False:否; 默认值是True;
    (7).option_list:当前脚本程序的命令行选项列表;这个选项列表在standard_options_list中选项添加之后,但是在版本和帮助选项添加之前;可以手工创建该列表,该列表中的元素都使用函数make_option()生成;
    例如:option_list=[make_option("-f","--file",action="store",type="string",dest="filename"), ...];
    (8).option_class:在使用函数add_option()添加命令行选项到解析器时使用的类;默认为optparse.Option类;
    (9).version:打印版本的信息;
    (10).formatter:帮助信息格式;有两种格式:IndentedHelpFormatter和TitledHelpFormatter;
    其中,参数prog在usage和version中使用格式字符串"%prog"代替os.path.basename(sys.argv[0]);
    """
    parser = optparse.OptionParser(**compat_kwargs(kw))

    # 分组选项
    # ===================================================================================================================
    # 基础选项

    """
    optparse.OptionGroup(parser,title,description=None)
        * parser是OptionParser实例插入到组中的
        * title是组的标题
        * description，optional是组的长描述信息
    """
    general = optparse.OptionGroup(parser, 'General Options')
    # 每个选项都有一个或多个选项字符串，如 -f 或 --file 和几个选项属性用于告诉optparse当在命令行中遇到选项是你期望声明和它该做什么。
    """
    选项行为action的理解: 告诉当在命令行遇到选项时应该做什么
    * 不指定的, 默认为store
    * 'store': 下一个参数(或当前参数的其余部分)存储到选择的目的地('dest')
    * 'store_true': 设定选项为真
    * 'store_false': 设定选项为假
    * 'store_const': 存储常量值
    * 'append': 将选项的参数增加到列表中
    * 'count': 增加一个计数器
    * 'callback: 调用一个指定的函数
    """

    # 帮助
    general.add_option(
        '-h', '--help',
        action='help',
        help='Print this help text and exit'
    )
    # 版本
    general.add_option(
        '-v', '--version',
        action='version',
        help='Print program version and exit'
    )
    # 更新
    general.add_option(
        '-U', '--update',
        action='store_true', dest='update_self',
        help='Update this program to latest version. Make sure that you have suffcient permissions (run with sudo if needed)'
    )
    # 如果发生错误, 继续其他下载
    general.add_option(
        '-i', '--ignore-errors',
        aciton='store_true', dest='ignoreerrors', default=False,
        help='Continue on download errors, for example to skip unavailable videos in playlist'
    )
    # 如果发生错误, 终止下载其他视频
    general.add_option(
        '--abort-on-error',
        action='store_false', dest='ignorerrors',
        help='Abort downloading of furthur videos (in the playlist or the command line) if an error occurs'
    )
    # 显示当前浏览器标识 TODO：验证
    general.add_option(
        '--dump-user-agent',
        action='store_true', dest='dump-user-agent', default=False,
        help='Display the current browser identification'
    )
    # 列举支持提取视频的网站
    general.add_option(
        '--list-extractors',
        action='store_true', dest='list_extractors', default=False,
        help='List all supported extractors'
    )
    # 输出所有支持网站的描述
    general.add_option(
        '--extractor-descriptions',
        action='store_true', dest='list_extractor_descriptions', default=False,
        help='Output descriptions of all supported extractors'
    )
    # 强制使用通用提取器
    general.add_option(
        '--force-generic-extractor',
        action='store_true', dest='force_generic_extractor', default=False,
        help='Force extraction to use the generic extractor'
    )
    # TODO：如何使用
    general.add_option(
        '--default-search',
        dest='default_search', metavar='PREFIX',
        help='Use this prefix for unqualified URLs. For Example "gvsearch2:" download two videos from google videos for '
             'youtube-dl "large apple". Use the value "auto" to let youtube-dl guess. "error" just throws an error. The '
             'default value "fixup_error" repairs broken URLs, but emits an error '
             'if this is not possible instead of searching.'
    )
    # 忽略用户配置文件
    # 如果设置了全局配置文件(/etc/youtube-dl.conf),
    # 就不会读取用户配置文件(~/.config/youtube-dl/config) (%APPDATA%/youtube-dl/config.txt on windows)
    general.add_option(
        '--ignore-config',
        action='store_true',
        help='Do not read configuration files.'
    )
    # 配置文件的位置
    general.add_option(
        '--config-location',
        dest='config_location', metavar='PATH',
        help='Location of the configuration file; either the path to the config or its containing directory'
    )
    # 只列举视频列表, 不下载视频
    general.add_option(
        '--flat-playlist',
        action='store_const', dest='extract_flat', const='in_playlist',
        default=False,
        help='Do not extract the videos of a playlist, only list them.'
    )
    # 标记视频(仅支持 Youtube)
    general.add_option(
        '--mark-watched',
        action='store_true', dest='mark_watched', default=False,
        help='Mark videos wathched(Youtube only)'
    )
    # 不标记视频(仅支持 Youtube)
    general.add_option(
        '--no-mark-watched',
        action='store_false', dest='mark_watched', default=False,
        help='Do not mark videos watched (YouTube only)'
    )
    # 不要输出有颜色的代码
    general.add_option(
        '--no-color', '--no-colors',
        aciton='store_true', dest='no_color',
        default=False,
        help='Do not emit color codes in output'
    )

    #===================================================================================================================
    # 网络选项
    network = optparse.OptionGroup(parser, 'Network Options')

    # 指定代理
    network.add_option(
        '--proxy', dest='proxy', default=None, metavar='URL',
        help='Use the specified HTTP/HTTPS/SOCKS proxy. To enable experimental SOCKS proxy, specify a proper scheme. '
             'For example socks5://127.0.0.1:1080/. Pass in an empty string (--proxy "") for direct connection'
    )
    # 超时时间
    network.add_option(
        '--socket-timeout',
        dest='socket_timeout', type=float, default=None, metavar='SECONDS',
        help='Time to wait before giving up, in seconds'
    )
    # 绑定的客服端IP
    network.add_option(
        '--source-address',
        metavar='IP', dest='source-address', default=None,
        help='Client-side IP address to bind to'
    )
    # 通过IPv4进行所有连接
    network.add_option(
        '-4', '--force-ipv4',
        aciton='store_const', const='0.0.0.0', dest='source_address',
        help='Make all connections via IPv4'
    )
    # 通过IPv6进行所有连接
    network.add_option(
        '-6', '--force-ipv6',
        action='store_const', const='::', dest='source_address',
        help='Make all connections via IPv6'
    )

    # ===================================================================================================================
    # 地理限制
    geo = optparse.OptionGroup(parser, 'Geo Restriction')

    # 使用此代理验证受地理位置限制的站点的 IP地址。 --proxy 指定的默认代理用于实际下载
    geo.add_option(
        '--geo-verification-proxy',
        dest='geo_verification_proxy', default=None, metavar='URL',
        help='Use this proxy to verify the IP address for some geo-restricted sites. '
             'The default proxy specified by --proxy (or none, if the options is not present) is used for the actual downloading.'
    )
    #
    geo.add_option(
        '--cn-verification-proxy',
        dest='cn_verification_proxy', default=None, metavar='URL',
        help=optparse.SUPPRESS_HELP
    )
    # 通过伪造绕过地理限制X-Forwarded-For (测试阶段)
    geo.add_option(
        '--geo-bypass',
        action='store_true', dest='geo_bypass', default=True,
        help='Bypass geographic restriction via faking X-Forwarded-For HTTP header (experimental)'
    )
    # 不伪造
    geo.add_option(
        '--no-geo-bypass',
        action='store_false', dest='geo_bypass', default=True,
        help='Do not bypass geographic restriction via faking X-Forwarded-For HTTP header (experimental)'
    )
    # 强制绕过地理限制, 提供 ISO 316602 提供的2字符国家代码
    geo.add_option(
        '--geo-bypass-country', metavar='CODE',
        dest='geo_bypass_country', default=None,
        help='Force bypass geographic restriction with explicitly provided two-letter ISO 316602 country code (experimental)'
    )

    # ===================================================================================================================
    # 视频选择
    selection = optparse.OptionGroup(parser, 'Video Selection')
    # 列表开始位置
    selection.add_option(
        '--playlist-start',
        dest='playliststart', metavar='NUMBER', default=1, type=int,
        help='Playlist video to start at (default is %default)'
    )
    # 列表结束位置
    selection.add_option(
        '--playlist-end',
        dest='playlistend', metavar='NUMBER', default=None, type=int,
        help='Playlist video to end at (default is last)'
    )
    # 指定下载的视频项
    selection.add_option(
        '--playlist-items',
        dest='playlist_items', metavar='ITEM_SPEC', default=None,
        help='Playlist video items to download. Specify indices of the video in the playlist separated by commas like:'
             '"--playlist-items 1,2,5,8" if you want to download videos indexed 1, 2, 5 8 in the playlist, you can specify'
             'range: "--playlist-items 1-3,7,10-13", it will download the videos at index 1, 2, 3, 7, 10, 11, 12 and 13.'
    )
    # 下载匹配标题的视频
    selection.add_option(
        '--match-title',
        dest='rejecttitle', metavar='REGEX',
        help='Download only matching titles (regex or caseless sub-string)'
    )
    # 设置最大下载数量
    selection.add_option(
        '--max-downloads',
        dest='max_downloads', metavar='NUMBER', type=int, default=None,
        help='Abort after downloading NUMBER files'
    )
    # 设置下载文件的最小大小
    selection.add_option(
        '--min-filesize',
        metavar='SIZE', dest='min_filesize', default=None,
        help='Do not download any videos smaller than SIZE (e.g. 50k or 44.6m)'
    )
    # 设置下载文件的最大大小
    selection.add_option(
        '--max-filesize',
        metavar='SIZE', dest='max_filesize', default=None,
        help='Do not download any videos larger than SIZE (e.g. 50k or 44.6m)'
    )
    # 仅下载在此日期上传的视频
    selection.add_option(
        '--date',
        metavar='DATE', dest='date', default=None,
        help='Download only videos uploaded in this date'
    )
    # 仅下载在此日期之前或之前上传的视频（即包含）
    selection.add_option(
        '--datebefore',
        metavar='DATE', dest='datebefore', default=None,
        help='Download only videos uploaded on or before this date (i.e. inclusive)'
    )
    # 仅下载在此日期之前或之后上传的视频（即包含）
    selection.add_option(
        '--dateafter',
        metavar='DATE', dest='dateafter', default=None,
        help='Download only videos uploaded on or after this date (i.e. inclusive)'
    )
    # 不要下载少于COUNT次观看次数的视频
    selection.add_option(
        '--min-views',
        metavar='COUNT', dest='min_views', default=None, type=int,
        help='Do not download any videos with less than COUNT views'
    )
    # 不要下载大于COUNT次观看次数的视频
    selection.add_option(
        '--max-views',
        metavar='COUNT', dest='max_views', default=None, type=int,
        help='Do not download any videos with more than COUNT views'
    )

    parser.add_option_group(general)
    parser.add_option_group(network)
    parser.add_option_group(geo)

    if overrideArguments is not None:
        opts, args = parser.parse_args(overrideArguments)
        if opts.verbose:
            write_string('[debug] Override config:' + repr(overrideArguments) + '\n')
    else:
        def compat_conf(temp):
            if sys.version_info < (3,):
                return [a.decode(preferredencoding(), 'replace') for a in temp]
            return temp

        command_line_conf = compat_conf(sys.argv[1:])
        opts, args = parser.parse_args(command_line_conf)

        system_conf = user_conf = custom_conf = []

        if '--config-location' in command_line_conf:
            location = compat_expanduser(opts.config_location)
            if os.path.isdir(location):
                location = os.path.join(location, 'youtube-dl.conf')
            if not os.path.exists(location):
                parser.error('config-location %s does not exist.' % location)
            custom_conf = _readOptions(location)
        elif '--ignore-config' in command_line_conf:
            pass
        else:
            system_conf = _readOptions('/etc/youtube-dl.conf')
            if '--ignore-config' not in system_conf:
                user_conf = _readUserConf()

        argv = system_conf + user_conf + custom_conf + command_line_conf
        opts, args = parser.parse_args(argv)
        if opts.verbose:
            for conf_label, conf in (
                    ('System config', system_conf),
                    ('User config', user_conf),
                    ('Custom config', custom_conf),
                    ('Command-line args', command_line_conf)):
                write_string('[debug] %s: %s\n' % (conf_label, repr(_hide_login_info(conf))))

    return parser, opts, args

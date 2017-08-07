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


from compat import (
    compat_getpass,
    compat_shlex_split,
)

from options import (
    parseOpts,
)

from utils import (
    std_headers,
    expand_path,
    read_batch_urls,
    render_table,
    preferredencoding,
    write_string,
    DateRange,
    DEFAULT_OUTTMPL,
    match_filter_func,
    decodeOption,
)

from .downloader import FileDownloader
from .extractor import gen_extractors, list_extractors


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
            batch_urls = read_batch_urls(batchfd)
            if opts.verbose:
                write_string('[debug] Batch file urls: ' + repr(batch_urls) + '\n')
        except IOError:
            sys.exit('ERROR: batch file could not be read')
    # batch_urls 已经 去空白符了
    all_urls = batch_urls + [url.strip() for url in args]
    _enc = preferredencoding()
    all_urls = [url.decode(_enc, 'ignore') if isinstance(url, bytes) else url for url in all_urls]

    if opts.list_extractors:
        for ie in list_extractors(opts.age_limit):
            if not ie._WORKING:
                continue
            desc = getattr(ie, 'IE_DESC', ie.IE_NAME)
            if desc is False:
                continue
            if hasattr(ie, 'SEARCH_KEY'):
                _SEARCHES = (
                'cute kittens', 'slithering pythons', 'falling cat', 'angry poodle', 'purple fish', 'running tortoise',
                'sleeping bunny', 'burping cow')
                _COUNTS = ('', '5', '10', 'all')
                desc += ' (Example: "%s%s:%s" )' % (ie.SEARCH_KEY, random.choice(_COUNTS), random.choice(_SEARCHES))
            write_string(desc + '\n', out=sys.stdout)
        # 列举所有提取器, 停止继续执行程序
        sys.exit(0)
    if opts.ap_list_mso:
        # 列出所有支持的多系统操作员
        table = [[mso_id, mso_info['name']] for mso_id, mso_info in MSO_INFO.items()]
        write_string('Supported TV Providers:\n' + render_table(['mso', 'mso name'], table) + '\n', out=sys.stdout)
        sys.exit(0)

    # 冲突，缺失和错误选项的处理
    if opts.usenetrc and (opts.username is not None or opts.password is not None):
        parser.error('using .netrc conflicts with giving username/password')
    # 有密码却无用户名
    if opts.password is not None and opts.username is None:
        parser.error('account username missing\n')
    # 有 TV-Provider 密码而没有账户名
    if opts.ap_password is not None and opts.ap_username is None:
        parser.error('TV Provider account username missing\n')
    #
    if opts.outtmpl is not None and (opts.usetitle or opts.autonumber or opts.useid):
        parser.error('using output template conflicts with using title, video ID or auto number')
    if opts.autonumber_size is not None:
        if opts.autonumber_size <= 0:
            parser.error('auto number size must be positive')
    if opts.autonumber_start is not None:
        if opts.autonumber_start < 0:
            parser.error('auto number start must be positive or 0')
    if opts.usetitle and opts.userid:
        parser.error('using title conflicts with using video ID')
    # 有用户名无密码, 提示用户输入密码
    if opts.usename is not None and opts.password is None:
        opts.password = compat_getpass('Type account password and press [Return]: ')
    if opts.ap_username is not None and opts.ap_password is None:
        opts.ap_password = compat_getpass('Type TV provider account password and press [Return]: ')
    # 处理 ratelimit, 如果不能转换成以 bytes 为单位的整数, 则报错
    if opts.ratelimit is not None:
        numeric_limit = FileDownloader.parse_bytes(opts.ratelimit)
        if numeric_limit is None:
            parser.error('invalid rate limit specified')
        opts.ratelimit = numeric_limit
    if opts.min_filesize is not None:
        numeric_limit = FileDownloader.parse_bytes(opts.min_filesize)
        if numeric_limit is None:
            parser.error('invalid min_filesize specified')
        opts.min_filesize = numeric_limit
    if opts.max_filesize is not None:
        numeric_limit = FileDownloader.parse_bytes(opts.max_filesize)
        if numeric_limit is None:
            parser.error('invalid max_filesize specified')
        opts.max_filesize = numeric_limit
    if opts.sleep_interval is not None:
        if opts.sleep_interval < 0:
            parser.error('sleep interval must be positive or 0')
    if opts.max_sleep_interval is not None:
        if opts.max_sleep_interval < 0:
            parser.error('max sleep interval must be positive or 0')
        if opts.max_sleep_interval < opts.sleep_interval:
            parser.error('max sleep interval must be greater than or equal to min sleep interval')
    else:
        opts.max_sleep_interval = opts.sleep_interval
    if opts.ap_mso and opts.ap_mso not in MSO_INFO:
        parser.error('Unsupported TV Provider, use --app-list-mso to get a list of supported TV Providers')

    # retries 重试   parse 解析
    def parse_retries(retries):
        if retries in ('inf', 'infinite'):
            parsed_retries = float('inf')
        else:
            try:
                parsed_retries = int(retries)
            except (TypeError, ValueError):
                parser.error('invalid retry count specified')
        return parsed_retries
    if opts.retries is not None:
        opts.retries = parse_retries(opts.retries)
    if opts.fragment_retries is not None:
        opts.fragment_retries = parse_retries(opts.fragment_retries)
    if opts.buffersize is not None:
        numeric_buffersize = FileDownloader.parse_bytes(opts.buffersize)
        if numeric_buffersize is None:
            parser.error('invalid buffer size specified')
        opts.buffersize = numeric_buffersize
    if opts.playliststart <= 0:
        raise ValueError('Playlist start must be positive')
    if opts.playlistend not in (-1, None) and opts.playlistend < opts.playliststart:
        raise ValueError('Playlist end must be greater than playlist start')
    if opts.extractaudio:
        if opts.audioformat not in ['best', 'aac', 'flac', 'mp3', 'm4a', 'opus', 'vorbis', 'wav']:
            parser.error('invalid audio format specified')
    if opts.audioquality:
        opts.audioquality = opts.audioquality.strip('k').strip('K')
        if not opts.audioquality.isdigit():
            parser.error('invalid audio quality specified')
    if opts.recodevideo is not None:
        if opts.recodevideo not in ['mp4', 'flv', 'webm', 'ogg', 'mkv', 'avi']:
            parser.error('invalid video recode format specified')
    if opts.convertsubtitles is not None:
        if opts.convertsubtitles not in ['srt', 'vtt', 'ass']:
            parser.error('invalid subtitle format specified')
    # 日期
    if opts.date is not None:
        date = DateRange.day(opts.date)
    else:
        date = DateRange(opts.dateafter, opts.datebefore)
    # 不下载视频
    if opts.extractaudio and not opts.keepvideo and opts.format is None:
        opts.format = 'bestaudio/best'
    # --all-sub 自动设置--write-sub  subtitles===>字幕
    if opts.allsubtitles and not opts.writeautomaticsub:
        opts.writesubtitles = True
    # 输出名称模板
    outtmpl = ((opts.outtmpl is not None and opts.outtmpl) or
               (opts.format == '-1' and opts.usetitle and '%(title)s-%(id)s-%(format)s.%(ext)s') or
               (opts.format == '-1' and '%(id)s-%(format)s.%(ext)s') or
               (opts.usetitle and opts.autonumber and '%(autonumber)s-%(title)s-%(id)s.%(ext)s') or
               (opts.usetitle and '%(title)s-%(id)s.%(ext)s') or
               (opts.useid and '%(id)s.%(ext)s') or
               (opts.autonumber and '%(autonumber)s-%(id)s.%(ext)s') or
               DEFAULT_OUTTMPL)
    if not os.path.splitext(outtmpl)[1] and opts.extractaudio:
        parser.error('Cannot download a video and extract audio into the same'
                     ' file! Use "{0}.%(ext)s instead of "{0}" as the output'
                     ' template'.format(outtmpl))

    any_setting = opts.geturl or opts.gettitle or opts.getid or opts.getthumbnail or opts.getdescription or \
                  opts.getfilename or opts.getformate or opts.getduration or opts.dumpjson or opts.dump_single_json
    any_printing = opts.print_json
    download_archive_fn = expand_path(opts.download_archive) if opts.download_archive is not None else opts.download_archive

    # PostProcessors 后置处理器
    postprocessors = []
    if opts.metafromtitle:
        postprocessors.append({
            'key': 'MetadataFromTitle',
            'titleformat': opts.metafromtitle
        })
    if opts.extractaudio:
        postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': opts.audioformat,
            'preferredquality': opts.audioquality,
            'nopostoverwrites': opts.nopostoverwrites
        })
    if opts.recodevideo:
        postprocessors.append({
            'key': 'FFmpegVideoConvertor',
            'preferredformat': opts.recodevideo,
        })
    # FFmpegMetadataPP应在FFmpegVideoConvertorPP和FFmpegExtractAudioPP元数据（3gp，webm等）之后运行。
    # 此后处理器应放在操纵后处理器（FFmpegEmbedSubtitle）的其他元数据之前，以防止额外的元数据丢失。
    # 默认情况下，ffmpeg保留适用于源和目标容器的元数据。 从这一点来看，容器不会改变，所以可以在这里添加元数据。
    if opts.addmetadata:
        postprocessors.append({'key': 'FFmpegMetadata'})
    if opts.convertsubtitles:
        postprocessors.append({
            'key': 'FFmpegSubtitlesConvertor',
            'format': opts.convertsubtitles
        })
    if opts.embedsubtitles:
        postprocessors.append({'key': 'FFmpegEmbedSubtitle'})
    if opts.embedthumbnail:
        already_have_thumbnail = opts.writethumbnail or opts.write_all_thumbnails
        postprocessors.append({
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': already_have_thumbnail
        })
        if not already_have_thumbnail:
            opts.writethumbnail = True
    # XAttrMetadataPP 应该在 post-processors 执行, 因为该操作可能会修改文件
    if opts.xattrs:
        postprocessors.append({'key': 'XAttrMetadata'})
    # 请保持ExecAfterDownload到底部，因为它允许用户以任何方式修改最终文件。
    # 因此，如果用户能够在您的后处理程序运行之前删除该文件，可能会导致一些问题。
    if opts.exec_cmd:
        postprocessors.append({
            'key': 'ExecAfterDownload',
            'exec_cmd': opts.exec_cmd
        })
    external_downloader_args = None
    if opts.external_downloader_args:
        external_downloader_args = compat_shlex_split(opts.external_downloader_args)
    postprocessors_args = None
    if opts.postprocessors_args:
        postprocessors_args = compat_shlex_split(opts.postprocessors_args)
    match_filter = (
        None if opts.match_filter is None
        else match_filter_func(opts.match_filter)
    )

    ydl_opts = {
        'usenetrc': opts.usenetrc,
        'username': opts.username,
        'password': opts.password,
        'twofactor': opts.twofactor,
        'videopassword': opts.videopassword,
        'ap_mso': opts.ap_mso,
        'ap_username': opts.ap_username,
        'ap_password': opts.ap_password,
        'quiet': (opts.quiet or any_setting or any_printing),
        'no_warnings': opts.no_warnings,
        'forceurl': opts.geturl,
        'forcetitle': opts.gettitle,
        'forceid': opts.getid,
        'forcethumbnail': opts.getthumbnail,
        'forcedescription': opts.getdescription,
        'forceduration': opts.getduration,
        'forcefilename': opts.getfilename,
        'forceformat': opts.getformat,
        'forcejson': opts.dumpjson or opts.print_json,
        'dump_single_json': opts.dump_single_json,
        'simulate': opts.simulate or any_setting,
        'skip_download': opts.skip_download,
        'format': opts.format,
        'listformats': opts.listformats,
        'outtmpl': outtmpl,
        'autonumber_size': opts.autonumber_size,
        'autonumber_start': opts.auonumber_start,
        'restrictfilenames': opts.restrictfilenames,
        'ignoreerrors': opts.ignoreerrors,
        'force_generic_extractor': opts.force_generic_extractor,
        'ratelimit': opts.ratelimit,
        'nooverwrites': opts.nooverwrites,
        'retries': opts.retries,
        'fragment_retries': opts.fragment_retries,
        'skip_unavailable_fragments': opts.skip_unavailable_fragments,
        'keep_fragments': opts.keep_fragments,
        'buffersize': opts.buffersize,
        'noresizebufer': opts.noresizebuffer,
        'continuedl': opts.continue_dl,
        'noprogress': opts.noprogress,
        'progress_with_newline': opts.progress_with_newline,
        'playliststart': opts.playliststart,
        'playlistend': opts.playlistend,
        'playlistreverse': opts.playlist_reverse,
        'playlistrandom': opts.playlist_random,
        'noplaylist': opts.noplaylist,
        'logtostderr': opts.outtmpl == '-',
        'consoletitle': opts.consoletitle,
        'nopart': opts.nopart,
        'updatetime': opts.updatetime,
        'writedescription': opts.writedescription,
        'writeannotations': opts.writeannotations,
        'writethumbnail': opts.writethumbnail,
        'write_all_thumbnail': opts.write_all_thumbnails,
        'writesubtitles': opts.writesubtitles,
        'writeautomaticsub': opts.writeautomaticsub,
        'allsubtitles': opts.allsubtitles,
        'listsubtitles': opts.listsubtitles,
        'subtitlesformat': opts.subtitlesformat,
        'subtitleslangs': opts.subtitleslangs,
        'matchtitle': decodeOption(opts.matchtitle),
        'rejecttitle': decodeOption(opts.rejecttitle),
        'max_downloads': opts.max_downloads,
        'prefer_free_formats': opts.prefer_free_formats,
        'verbose': opts.verbose,
        'dump_intermediate_pages': opts.dump_intermediate_pages,
        'write_pages': opts.write_pages,

    }


def main(argv=None):
    try:
        _real_main(argv)
    except DownloadError:
        sys.exit(1)
    except SameFileError:
        sys.exit('ERROR: fixed output name but more than one file to download')
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')


__all__ = ['main', 'YoutubeDL', 'gen_extractors', 'list_extractors']
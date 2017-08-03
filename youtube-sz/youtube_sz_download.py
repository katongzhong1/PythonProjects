#!/usr/bin/env python
# coding: utf-8

import youtube_dl

def my_hook(d):
    print(d)
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'progress_hooks': [my_hook],
    'download_archive': '~/Desktop/video/'
}

def download_url(url=None):
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

download_url('https://www.pornhub.com/view_video.php?viewkey=ph5925e5d459735')

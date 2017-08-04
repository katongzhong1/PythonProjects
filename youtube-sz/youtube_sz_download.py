#!/usr/bin/env python
# coding: utf-8

import youtube_dl
import socket
import random
import netifaces as ni
import urllib2
import re

true_socket = socket.socket
ipList=[]


class bindIp():
    ip = ''
    global true_socket, ipList

    def bound_socket(self,*a, **k):
        sock = true_socket(*a, **k)
        sock.bind((self.ip, 0))
        return sock

    def changeIp(self, ipaddress):
        self.ip = ipaddress
        if not self.ip == '':
            socket.socket = self.bound_socket
        else:
            socket.socket = true_socket

    def randomIp(self):
        if len(ipList) == 0:
            self.getLocalEthIps()
        if len(ipList) == 0:
            return
        _ip = random.choice(ipList)
        if not _ip == self.ip:
            self.ip = _ip
            self.changeIp(_ip)

    def getIp(self):
        return self.ip

    def getIpsCount(self):
        return len(ipList)

    def getLocalEthIps(self):
        for dev in ni.interfaces():
            print(dev)
            if dev.startswith('eth0'):
                ip = ni.ifaddresses(dev)[2][0]['addr']
                if ip not in ipList:
                    ipList.append(ip)

def my_hook(d):
    print(d)
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'progress_hooks': [my_hook],
    'writeinfojson': True,
    'writethumbnail': True
}

def download_url(url=None):
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

#download_url('https://www.youtube.com/watch?v=8bvKMzUaDGw')

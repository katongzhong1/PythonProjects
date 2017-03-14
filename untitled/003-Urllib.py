# !/usr/bin/env Python
# coding: utf-8

import urllib
import requests


def go(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print "%.2f%%" % per

url = "http://image61.360doc.com/DownloadImg/2013/05/1518/32353731_21.jpg"
local = "/Users/wushengzhong/Desktop/g.jpg"
urllib.urlretrieve(url, local, go)


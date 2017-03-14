# !/usr/bin/env python
# coding: utf-8

import urllib2
from pprint import pprint


request = urllib2.Request("http://www.baidu.com")
response = urllib2.urlopen(request)
pprint(response.read())


# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：6park爬虫
#   版本：0.1
#   作者：wushengzhong
#   日期：2013-05-14
#   语言：Python 2.7
#   操作：输入带分页的地址，去掉最后面的数字，设置一下起始页数和终点页数。
#   功能：下载对应页码内的所有页面并存储为html文件。
#---------------------------------------

import urllib2
import re
import json

URL = "http://site.6park.com/gz2/index.php"

class Park6Spider():
    def __init__(self):
        pass

    # 获取类型和地址
    def get_title_items(self):
        titles = self.get_arr("",
                             '<td><center>.*?<a href=(.*?)>(.*?)</a>.*?</center></td>',
                             '')
        for title in titles:
            url = title[0]
            # 移除空格之后的字符串和"符号
            url = url.split(' ')[0]
            url =  url.lstrip('"\'').rstrip('"\'')
            print('name:' + title[1] + '==>' + url)

    def get_arr(self, param, restr1, restr2):
        uri = URL + param
        request = urllib2.Request(uri)
        response = urllib2.urlopen(request)
        page = response.read()
        unpage = page.decode('GBK')
        if len(restr2):
            return self.get_items(unpage, restr1), self.get_items(unpage, restr2)
        return self.get_items(unpage, restr1)

    @staticmethod
    def get_items(page, restr):
        return re.findall(restr, page, re.S)

# ----------- 程序的入口处 -----------
print u"""
---------------------------------------
   程序：6park爬虫
   版本：1.0
   作者：zhong
   日期：2017-03-27
   语言：Python 2.7
   操作：
   功能：
---------------------------------------
"""

spider = Park6Spider()
spider.get_title_items()

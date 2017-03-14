# -*- coding: utf-8 -*-
# ---------------------------------------
#   程序：NipponColors 颜色
#   版本：1.0
#   作者：katongzhong
#   日期：2017-03-06
#   语言：Python 2.7
#   操作：
#   功能：
# ---------------------------------------

import urllib2
import re

URL = "http://nipponcolors.com/"


# ----------- 加载处理糗事百科 -----------
class SpiderModel:
    def __init__(self):
        pass

    # 将所有的段子都扣出来，添加到列表中并且返回列表
    def get_page(self):
        items = self.get_arr("", '<li id="col.*?"><div><a href=.*?>(.*?)</a></div></li>', '')
        for item in items:
            print item
            self.get_RGB(item)
        return items

    # 用于取到色值
    def get_RGB(self, param):
        arr = param.split(", ")
        #name = arr[0]
        tup = self.get_arr('#' + arr[1].lower(),
                           '<dd class=".*?"><span>(.*?)</span></dd>',
                           '<div id="RGBvalue"><input type="text" value="#(.*?)" readonly="readonly"></div>')
        print tup[0] + tup[1]
        return tup

    def get_arr(self, param, restr1, restr2):
        uri = URL + param
        request = urllib2.Request(uri)
        response = urllib2.urlopen(request)
        page = response.read()
        unpage = page.decode("utf-8")
        if len(restr2):
            return self.get_items(unpage, restr1), self.get_items(unpage, restr2)
        return self.get_items(unpage, restr1)

    @staticmethod
    def get_items(page, restr):
        return re.findall(restr, page, re.S)


# ----------- 程序的入口处 -----------
print u"""
---------------------------------------
   程序：NipponColors 颜色爬虫
   版本：1.0
   作者：zhong
   日期：2017-03-06
   语言：Python 2.7
   操作：
   功能：
---------------------------------------
"""

myModel = SpiderModel()
myModel.get_page()

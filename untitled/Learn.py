# -*- coding: utf-8 -*-

# name = raw_input("What's your name?")
# age = raw_input("How old are you?")

# print "Your name is:", name
# print "You are " + age + " years old."
#
# after_ten = int(age) + 10
# print "You will be " + str(after_ten) + " years old after tem years."


lang = "studyPython"
c = lang[:]
print id(c)
print id(lang)

print id(lang[1:])

print c == lang
print c in lang

print max(lang)
print min(lang)

print cmp('string', 'blx')
print ord('c')
print chr(98)

print lang * 3
print "-" * 20

print len(lang)

# 字符串的格式化输出
print "\n\n\n" + "==" * 10 + "字符串的格式化输出" + "==" * 10

print "%d years" % 15
print "%d years old, %.2f high" % (33, 1.798)
s2 = "{year} years old, {high} high".format(year="33", high="100")
print "I love %(pro)s" % {"pro": lang}
print s2

'''
>>> dir(str)
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
 '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__',
 '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__',
 '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser',
 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', 'isalnum',
 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition',
 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip',
 'swapcase', 'title', 'translate', 'upper', 'zfill']
'''

# split 分割函数
print "I LOVE PYTHON".split(" ")
# isalpha 判断是否全是字母
print "python".isalpha()
# strip lstrip rstrip 去掉空格
print " python ".strip()
# upper lower capitalize isupper islower istitle 大小写转化
print "qiwsir, Python".upper()
print "Qiwsir".istitle()
print "Qiwsir, Python".istitle()
print "Qiwsir, python".istitle()
print "this is a book".title()    # 这样可以把所有单词的第一个字母转化为大写
# join 拼接字符串
print ".".join(['www', 'baidu', 'com'])
# encode 字符编码
print '老'

# 列表
print "\n\n\n" + "==" * 10 + "列表" + "==" * 10
a = ['2', 3, 'github.io']
b = [4, 5, 6]
print a

# 索引和切片
print a[0]
print a[:2]
print a.index('2')
# 反转
print a[::-1]
print list(reversed(a))
# len 长度
print len(a)
# + 连接
print a+b
# * 重复元素
print a*2
# in 列表是否存在值
print '2' in a
# max() min()
print max(a)
print min(b)
# cmp() 比较列表
print cmp(a, b)
# append 追加元素
print b.append(7)  # 并不存在返回值
print b
# print b[3:]=[8]
b.extend('8')
print b

'''
>>> dir(list)
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__'
    , '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__',
 '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
 '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__',
 '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
'''
a.append(8)
print a
a.extend(b)
print a
a.extend("abc")
print a

# iterable 迭代
print hasattr("Python", '__iter__')
# count 计算某个元素的个数
print "===> count 计算某个元素的个数"
a = [1, 2, 1, 1, 3]
print a.count(1)
# insert 插入元素
print "===> insert 插入元素"
a.insert(0, 8)
print a
# pop remove 删除元素
print "===> pop remove 删除元素"
a.remove(2)
print a
a.pop(4)
print a
# in
if 2 in a:
    a.remove(2)
    print a
else:
    print "2 is not in a"
# reverse 反转
a.reverse()
print a
# sort 排序
a = [3, 4, 6, 2, 1]
a.sort(reverse=True)
print a

# 元组
print "\n\n\n" + "==" * 10 + "元组" + "==" * 10

t = 2, 3
print t

# 字典
print "\n\n\n" + "==" * 10 + "字典" + "==" * 10
person = {"name": "qiwsir", "site": "qiwsir.github.io", "language": "python"}
print person
# 利用元组构建字典
person = ([1, 2], ['value1', 'value2'])
website = dict(person)
print website
website = {}.fromkeys(("third", "forth"), "facebook")
print website
website = dict(name='katongzhong', age='26')
print website
# len(d) 字典中键值对的数量
# d[key] 返回字典中键的值
# d[key]=value 将值赋给字典中的键
# del d[key] 删除字典的键项
# key in d 检查字典中是否含有键为key的项
# copy deepcopy 浅拷贝\深拷贝
# clear 清空所有元素
# del 删除字典
# get 获得元素的值
website = {}.fromkeys(("third", "forth"), "facebook")
print website.get("five", 'baidu')
# setdefault
print website.setdefault("five", 'baidu')
print website
# items/iteritems, keys/iterkeys, values/itervalues
print website.items()
print list(website.iteritems())

# file
f = open('/Users/wushengzhong/Desktop/ufenqiiosapp/ufenqi/ufenqi/UFQServiceCenter.m', "r+")
print type(f)
for line in f:
    if "_currentUrl = @" in line:
        print line
f.close()


import random

score = [random.randint(0, 100) for i in range(40)];
print score

num = len(score)
sum = sum(score)
ave_num = sum/num
print sorted(score, reverse=True)


a, b = 0, 1
for i in range(4):
    a, b = b, a+b
print a


print filter(lambda c: c != 'i', 'qiwsir')
a = [3, 9, 8, 5, 2]
b = [1, 4, 9, 2, 6]
print map(lambda x, y: x+y, a, b)
print reduce(lambda x, y: x+y, map(lambda x, y: x*y, a, b))


from pprint import pprint as pt

a = {}.fromkeys(("lang", "book", "1", "2", "3", "4", "5", "6"), "www.baidu.com")
print a
print pt(a)

import sys

pt(sys.__doc__)
print "The file name: ", sys.argv[0]
print "The number of argument ", len(sys.argv)
print "The argument is: ", str(sys.argv)

import os

print os.listdir(os.getcwd())
p = os.getcwd()
print os.stat(p)

import time

print time.ctime(os.stat(p)[8])

import webbrowser


import calendar

cal = calendar.month(2015, 1)
print cal


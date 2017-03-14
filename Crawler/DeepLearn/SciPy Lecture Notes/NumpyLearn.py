# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：SciPy Lecture Notes
#   版本：1.0
#   作者：zhong
#   日期：2017-01-20
#   语言：Python 2.7
#   操作：
#   功能：
#---------------------------------------

import numpy as np

a = np.array([[0, 1, 2], [3, 4, 5]])

print(a)

# 维数
print(a.ndim)
# 2x3 数组
print(a.shape)

print('======================array')
b = np.arange(10) # 0 .. n-1 (!)
print(b)
print(np.arange(1, 25, 2))
print(np.linspace(0, 1, 5, endpoint=False))

print(np.ones((3, 3)))
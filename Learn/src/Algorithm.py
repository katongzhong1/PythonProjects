# -*- coding: utf-8 -*-
# ---------------------------------------
#   程序：算法 学习
#   版本：1.0
#   作者：katongzhong
#   日期：2017-03-03
#   语言：Python 2.7
#   操作：
#   功能：
# ---------------------------------------


class SZAlgorithm:
    def __init__(self):
        pass

    """
    # 最大公约数 commondivisor
    # 两个数的最大公约数
    # 计算两个非负整数p和q的最大公约数： 若q是0， 则最大公约数为p。
    # 否则， 将p除以q得到余数r，p和q的最大公约数即为q和r的最大公约数。
    """
    def gcd(self, p, q):
        if q == 0:
            return p
        else:
            r = p % q
            return self.gcd(q, r)

class SZSort:
    def __init__(self):
        pass

    def less(self, a, b):
        return cmp(a, b)

    def sort_selection(self, a):
        for i in range(0, len(a)):
            min = i;
            for j in range(0, len(a)):
                if cmp(a[i], a[j]):
                    min = j;



# 最大公约数
print SZAlgorithm().gcd(10, 4)
#
print (1 + 2.236) / 2
#
sum = 0
for i in range(1, 1000, )


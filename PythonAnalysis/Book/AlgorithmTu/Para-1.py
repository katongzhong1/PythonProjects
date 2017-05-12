# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：Python算法教程
#   版本：1.0
#   作者：zhong
#   日期：2017-04-24
#   语言：Python 2.7
#---------------------------------------

#记时操作
import timeit

# 二叉树
class Tree:
    def __init__(self, left, right):
        self.left = left
        self.right = right


# 多路搜索树
class MultiTree:
    def __init__(self, kids, next=None):
        self.kids = self.val = kids
        self.next = next

# Bunch 模式
class Bunch(dict):
    def __init__(self, *args, **kwds):
        super(Bunch, self).__init__(*args, **kwds)
        self.__dict__ = self

# 图结构库
# ==> a. NetworkX
#     b. python-graph
#     c. Graphine
#     d. Graph-tool:

#
print(0.1)
print(sum(0.1 for i in range(10)) == 1.0)

# 求和式的书写
x = 3
S = [1, 2, 3]
print(sum(x*y for y in S))
print(x * sum(S))

# 两种赛制的故事
# 循环赛 比赛场次为 n * (n - 1) / 2 为 Θ(n**2)
# 淘汰赛 比赛场次为 n - 1

# 排序算法之: 侏儒排序法
# ==> a. 最好情况: 目标序列已经排好序, 运行时间为Θ(n)
#     b. 最坏情况: 每发现一个元素都需要移动最左边的位置, 故而最糟糕的运行时间为1+2+...+(n-1), 即Θ(n**2)
def gnomesort(seq):
    i = 0
    while i < len(seq):
        if i == 0 or seq[i-1] <= seq[i]:
            i += 1
        else:
            seq[i], seq[i-1] = seq[i-1], seq[i]
            i -= 1

# 排序算法之: 归并排序法
def mergesort(seq):
    mid = len(seq)/2
    lft, rgt = seq[:mid], seq[mid:]
    if len(lft) > 1: lft = mergesort(lft)
    if len(rgt) > 1: rgt = mergesort(rgt)
    res = []
    while lft and rgt:
        if lft[-1] >= rgt[-1]:
            res.append(lft.pop())
        else:
            res.append(rgt.pop())
    res.reverse()
    return (lft or rgt) + res

# 归纳(induction):
# ==> a. 用于证明某个语句对于某种大型对象类(通常是一些自然数类型)是否成立
# 递归(recursion):
# ==> a. 主要用于函数自我调用的时候。
# 归简(reduction):
# ==> a. 指将某一问题转化为另一个问题。
#     b. 通常将一个未知问题归简为一个已解决的问题。
#     c. 涉及输入(操作中可能会遇到的新问题)与输出(已经解决的原问题)之间的转化

# 棋盘拼接问题
def cover(board, lab=1, top=0, left=0, side=None):

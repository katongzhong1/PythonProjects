# -*- coding: utf-8 -*-
# ---------------------------------------
#   程序：定义表示直方图的 Hist 对象及表示 PMF的 Pmf 对象
#   版本：1.0
#   作者：zhong
#   日期：2017-04-18
#   语言：Python 2.7
#   操作：
#   功能：
# ---------------------------------------

import math
import random
import matplotlib.pyplot as pyplot

class _DictWrapper(object):
    """包含 dictionary 的对象"""

    def __init__(self, d=None, name=''):
        if d is None:
            d = {}
        self.d = d
        self.name = name

    def GetDict(self):
        return self.d

    def Values(self):
        """获取未排序的值序列"""
        return self.d.keys()

    def Items(self):
        return self.d.items()

    def Render(self):
        """生成适合绘图的点序列
        Returns:
            (排序值序列, 频数和概率序列)
        """
        return zip(*sorted(self.Items()))

    def Print(self):
        for val, prob in sorted(self.d.iteritems()):
            print(val, prob)

    def Set(self, x, y=0):
        self.d[x] = y

    def Incr(self, x, term=1):
        self.d[x] = self.d.get(x, 0) + term

    def Mult(self, x, factor):
        self.d[x] = self.d.get(x, 0) * factor

    def Remove(self, x):
        del self.d[x]

    def Total(self):
        return sum(self.d.itervalues())

    def MaxLike(self):
        return max(self.d.itervalues())


class Hist(_DictWrapper):
    def Copy(self, name=None):
        if name is None:
            name = self.name
        return Hist(dict(self.d), name)

    def Freq(self, x):
        """获取与值x相关联的频数"""
        return self.d.get(x, 0)

    def Freqs(self):
        return self.d.values()

    def IsSubset(self, other):
        """检查此直方图中的值是否是给定直方图中值的子集"""
        for val, freq in self.Items():
            if freq > other.Freq(val):
                return False
        return True

    def Subtract(self, other):
        """减去此直方图中在给定直方图中的值"""
        for val, freq in other.Items():
            self.Incr(val, -freq)

class Pmf(_DictWrapper):
    """表示概率质量函数"""

    def Copy(self, name=None):
        if name is None:
            name = self.name
        return Pmf(dict(self.d), name)

    def Prob(self, x, default=0):
        return self.d.get(x, default)

    def Probs(self):
        return self.d.values()

    def Normalize(self, fraction=1.0):
        total = self.Total()
        if total == 0.0:
            return

        factor = float(fraction) / total
        for x in self.d:
            self.d[x] *= factor

    def Random(self):
        """"""
        if len(self.d) == 0:
            raise ValueError('Pmf contains no values')

        target = random.random()
        total = 0.0
        for x, p in self.d.iteritems():
            total += p
            if total >= target:
                return x
        """不会走到这"""
        assert False

    def Mean(self):
        """计算均值"""
        mu = 0.0
        for x, p in self.d.iteritems():
            mu += p * x
        return mu

    def Var(self, mu=None):
        if mu is None:
            mu = self.Mean()

        var = 0.0
        for x, p in self.d.iteritems():
            var += p * (x - mu)**2
        return var

    def Log(self):
        m = self.MaxLike()
        for x, p in self.d.iteritems():
            self.Set(x, math.log(p/m))

    def Exp(self):
        """指定概率"""
        m = self.MaxLike()
        for x, p in self.d.iteritems():
            self.Set(x, math.exp(p-m))


def MakeHistFromList(t, name=''):
    hist = Hist(name=name)
    [hist.Incr(x) for x in t]
    return hist

def MakeHistFromDict(d, name=''):
    return Hist(d, name)

def MakePmfFromList(t, name=''):
    hist = MakeHistFromList(t, name)
    return MakePmfFromHist(hist)

def MakePmfFromDict(d, name=''):
    pmf = Pmf(d, name)
    pmf.Normalize()
    return pmf

def MakePmfFromHist(hist, name=None):
    if name is None:
        name = hist.name
    d = dict(hist.GetDict())
    pmf = Pmf(d, name)
    pmf.Normalize()
    return pmf

def MakePmfFromCdf(cdf, name=None):
    if name is None:
        name = cdf.name
    pmf = Pmf(name=name)
    prev = 0.0
    for val, prob in cdf.Items():
        pmf.Incr(val, prob-prev)
        prev = prob

    return pmf

def MakeMixture(pmfs, name='mix'):
    mix = Pmf(name=name)
    for pmf, prob in pmfs.Items():
        for x, p in pmf.Items():
            mix.Incr(x, p * prob)
    return mix


#test
hist = MakeHistFromList([1, 2, 2, 3, 5])
print(hist.Freq(2))
print(hist.Values())

vals, freqs = hist.Render()
rectangles = pyplot.bar(vals, freqs)
pyplot.show()




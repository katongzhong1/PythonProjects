# -*- coding: utf-8 -*-

import bisect
import random


def Mean(t):
    """计算一系列数字的均值"""
    return  float(sum(t)) / len(t)

def Var(t, mu=None):
    """计算数字序列的方差"""
    if mu is None:
        mu = Mean(t)

    dev2 = [(x - mu)**2 for x in t]
    var = Mean(dev2)
    return var

def MeanVar(t):
    """计算一系列数字的均值和方差"""
    mu = Mean(t)
    var = Var(t, mu)
    return  mu, var

def TrimmedMean(t, p=0.01):
    """计算修正系列数字的均值"""
    t = Trim(t, p)
    return Mean(t)

def TrimmedMeanVar(t, p=0.01):
    """计算修正系列数字的均值和方差"""
    t = Trim(t, p)
    mu, var = MeanVar(t)
    return mu, var

def Trim(t, p=0.01):
    """移除t中的最大和最小的元素
    Args:
        p: 值的百分比
    """
    n = int(p * len(t)) #移除的值的百分比
    t = sorted(t)[n:-n]
    return  t

def Jitter(values, jitter=0.5):
    """"""
    return [x + random.uniform(-jitter, jitter) for x in values]

def Binom(n, k, d={}):
    if k == 0:
        return 1
    if n == 0:
        return 0

    try:
        return d[n, k]
    except KeyError:
        res = Binom(n-1, k) + Binom(n-1, k-1)
        d[n, k] = res
        return res







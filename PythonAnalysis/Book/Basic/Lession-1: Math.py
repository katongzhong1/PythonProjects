# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：Python基础数类型和运算
#   版本：1.0
#   作者：zhong
#   日期：2017-04-24
#   语言：Python 2.7
#---------------------------------------

#=======================================================================================================================
# __future__ 模块
#=======================================================================================================================
# ==> 使用此模块, 必须是模块或程序的第一个语句
# ==> 从python2.1开始以后, 当一个新的语言特性首次出现在发行版中时候, 如果该新特性与以前旧版本python不兼容, 则该特性将会被默认禁用.
#     如果想启用这个新特性, 则必须使用 "from __future__import *" 语句进行导入.

# 导入此函数 除法时不管是什么类型的分子和分母, 得到的都是浮点数的结果
from __future__ import division
# 使得所有的字符串文本成为 Unicode 字符串
from __future__ import unicode_literals
# 禁止版本中的 print 'abc'的打印方式, python2中不需要括号, python3中需要括号
from __future__ import print_function
# with 特性, with 方式可以替换以前的 try..catch 语句
from __future__ import with_statement
# 看下面的释义
from __future__ import nested_scopes
# 使用生成器.
from __future__ import generators
#
from __future__ import absolute_import


# nested_scopes 表示嵌套作用域
# nested_scopes = _Feature((2, 1, 0, "beta",  1),
#                         (2, 2, 0, "alpha", 0),
#                         CO_NESTED)
# 理解: 2.1.0b1中出现, 2.2.0a0中成为标准
# 差别:
#     a. 2.0中, 当在一个嵌套函数或lambda 函数中引用了一个变量时, 现在当前函数的名称空间中搜索, 然后在模块的名称空间中搜索;
#        2.2 在当前的函数的名称空间中搜索, 然后在父函数的名称空间, 最后是模块的名称空间
# a. 命名的定义
#    ==> 1.Python 命名空间是名称到对象的映射, 目前用字典实现, 键名是变量名, 值是变量的值
#        e.g.
#               x = 3
#               print(globals())
#               print(locals())
#           同样也可以通过这样的形式
#               globals()['y'] = 3
#               print(y)
#           删除属性值
#               del x
#               print(globals())
#    ==> 2. 命名空间的种类
#        ==> a. 局部, 如函数内部的命名空间
#            b. 全局, 模块内的命名空间
#            c. 内置, 包括异常类型, 内建函数, 特殊方法
# b. 作用域(命名空间的可见性)
#    ==> a. 作用域是一个Python程序中命名空间直接可见的代码区域。
#        b. 内置命名空间在代码所有位置都是可见的, 可随时被调用
#        c. 全局和局部中, 如果有同名变量, 在全局命名空白处, 局部命名空间内的同名变量是不可见的
#           ==> 如下情况会报错 local variable 'a' referenced before assignment
#               a = 3
#               def add(para):
#                   temp = a + 3
#                   a = 4
#               return temp
#               print(add(3))
# c. 命名空间的查找顺序
#    ==> 1. 函数内的变量现在函数内查找, 如果没有找到则停止查找, 在函数外部查找, 如果还是没有找到则在内置命名空间查找
#           再如果都没有找到则抛出 NameError 的异常
#    ==> 2. 函数外调用  全局变量==>内置变量==>抛出异常(有种情况例外, 当局部命名空间内含有 globa关键字声明的一个变量时, 则同1.
# d. 由于现在都是2.7或3, 所以已经是嵌套作用域了

# generators
# 2.2.0a1中出现, 2.3.0f0中成为标准
# 1. 意义: 记住上一次返回时在函数体中的位置。
# 2. 代表: yield就是一个生成器
#    ==> yield生成器的运行机制
#        ==> 当找生成器要一个数时, 生成器会执行, 直至出现 yield 语句, 生成器会把 yield 的参数给你,
#            之后生成器就不会往下继续执行, 当要下一个数时, 会从上次的状态开始运行, 直至出现 yield 语句,
#            把参数给你, 之后停下, 如此反复直至退出函数
#

# unicode_literals 这样可以使打印出来的会是转义之后的字符串
print('\u751f\u3080\u304e\u3000\u751f\u3054''\u3081\u3000\u751f\u305f\u307e\u3054')
# division 使得得到的是浮点数的结果
print(5/2)
# 如果要得到整数的结果, 使用地板除 //
print(5//2)

#=======================================================================================================================
# 常见函数
#=======================================================================================================================

# ==> abs() 求绝对值
print(abs(-10))
# ==> round 四舍五入
print(round(1.234))
print(round(1.254, 2))
# ==> pow() 幂函数
print(pow(2, 3))
# ==> 得商得余
print(divmod(9, 2))

#=======================================================================================================================
# math 模块
#=======================================================================================================================
import math

# ==> 圆周率pi 值 3.14...
print(math.pi)
# ==> 自然常数e
print(math.e)
# ==> 弧度转度
print('> 弧度转度 pi')
print(math.degrees(math.pi))
# ==> 度转弧度
print('> 度转弧度 180')
print(math.radians(180))
# ==> e的x次方值
print('> e的x次方值')
print(math.exp(2))
# ==> e的x次方值减1
print('> e的x次方值减1')
print(math.expm1(2))
# ==> 返回x的以base为底的对数, base 默认为 e
print('> log(e)e 的值')
print(math.log(math.e))
# ==> 返回x的以10为底的对数
print('> 返回x的以10为底的对数')
print(math.log10(100))
# ==> 返回x+1的自然对数(以e为底)
print('> 返回x+1的自然对数(以e为底)')
print(math.log1p(math.e-1))
# ==> 返回 x 的 y 次方
print('> 返回 x 的 y 次方')
print(math.pow(2, 3))
# ==> 返回 x 的平方根
print('> 返回 x 的平方根')
print(math.sqrt(16))
# ==> 返回不小于x的整数
print('> 返回不小于x的整数')
print(math.ceil(4.9))
# ==> 返回不大于x的整数
print('> 返回不大于x的整数')
print(math.floor(4.9))
# ==> 返回x的整数部分
print('> 返回x的整数部分')
print(math.trunc(4.9))
# ==> 返回x的小数和整数
print('> 返回x的小数和整数')
print(math.modf(4.9))
# ==> 返回 x 的绝对值
print('> 返回 x 的绝对值')
print(math.fabs(-4.9))
# ==> 取余
print('> 取余')
print(math.fmod(5, 2))
# ==> 无损精度的和
print('> 无损精度的和')
print(math.fsum([0.1, 0.2, 0.3]))
# ==> x的阶乘
print('> x的阶乘')
print(math.factorial(5))
# ==> 判断是否为无穷大
print('> 判断是否为无穷大')
print(math.isinf(1.0e+308))
print(math.isinf(1.0e+309))
# ==> 判断是否为数字
print('> 判断是否为数字')
print(math.isnan(1.2e3))
# ==> 返回以 x和y 为直角边的斜边长
print('> 返回以 x和y 为直角边的斜边长')
print(math.hypot(3, 4))
# ==> 若y< 0, 则返回-1乘以x的绝对值; 否则返回x的绝对值
print('> 若y< 0, 则返回-1乘以x的绝对值; 否则返回x的绝对值')
print(math.copysign(5.2, -1))
# ==> 返回 m, i; 满足 m * 2**i = x
print('> 返回 m, i; 满足 m * 2**i = x')
print(math.frexp(3))
# ==> 返回 m * 2**i 的值
print('> 返回 m * 2**i 的值')
print(math.ldexp(0.75, 2))
# ==> 返回弧度的正弦值
print('> 返回弧度的正弦值')
print(math.sin(math.radians(30)))
# ==> 反正弦值 y = arcsin(x) 定义域为[-1, 1] 值域为[-π/2, π/2]
print('> 反正弦值')
print(math.asin(1)*2)
# ==> 余弦值
print('> 余弦值')
print(math.cos(math.radians(60)))
# ==> 反余弦值 y = arccos(x) 定义域为[-1, 1] 值域为[0, π]
print('> 反余弦值')
print(math.acos(0.5))
# ==> 正切值
print('> 正切值')
print(math.tan(math.pi/4))
# ==> 反正切值 y = arctan(x) 定义域为R 值域为(-π/2, π/2)
print('> 反正切值')
print(math.atan(60))
# ==> 返回x/y 的反三角正切值
print('> 返回x/y 的反三角正切值')
print(math.atan2(2, 1))
# ==> x的双曲正弦函数 y=sinh(x), 定义域：R，值域：R，奇函数，函数图像为过原点并且穿越Ⅰ、Ⅲ象限的严格单调递增曲线，函数图像关于原点对称
print('> x的双曲正弦函数')
print(math.sinh(2))
# ==> x的反双曲正弦函数
print('> x的反双曲正弦函数')
print(math.asinh(2))
# ==> x的双曲余弦函数 y=cosh x，定义域：R，值域：[1,+∞)，偶函数，函数图像是悬链线，最低点是（0，1），在Ⅰ象限部分是严格单调递增曲线，函数图像关于y轴对称
print('> x的双曲余弦函数')
print(math.cosh(2))
# ==> x的反双曲余弦函数
print('> x的反双曲余弦函数')
print(math.acosh(2))
# ==> x的双曲正切函数 y=tanh x，定义域：R，值域：(-1,1)，奇函数，函数图像为过原点并且穿越Ⅰ、Ⅲ象限的严格单调递增曲线，其图像被限制在两水平渐近线y=1和y=-1之间
print('> x的双曲正切函数')
print(math.tanh(2))
# ==> x的反双曲正切函数
print('> x的反双曲正切函数')
print(math.atanh(0.5))
# ==> 返回x的误差函数 亦称之为高斯误差函数
print('> 返回x的误差函数')
print(math.erf(3))
# ==> 返回x的余误差函数
print('> 返回x的余误差函数')
print(math.erfc(3))
# ==> 伽玛函数
print('> 伽玛函数')
print(math.gamma(6))
# ==> x的绝对值的自然对数的伽玛函数
print('> x的绝对值的自然对数的伽玛函数')
print(math.lgamma(3))
#


# @Author: 骆金参
# @Date:   2017-02-26T21:19:04+08:00
# @Email:  1095947440@qq.com
# @Filename: class-ch1-basic.py
# @Last modified by:   骆金参
# @Last modified time: 2017-04-01T15:35:42+08:00


#!/usr/bin/python3

class MyClass:
    """一个简单的类实例"""
    i = 12345
    def f(self):
        return 'hello world'

# 实例化类
x = MyClass()

# 访问类的属性和方法
print("MyClass 类的属性 i 为：", x.i)
print("MyClass 类的方法 f 输出为：", x.f())


class Test:
    def prt(self):
        print(self)
        print(self.__class__)


t = Test()
t.prt()

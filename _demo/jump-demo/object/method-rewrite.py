# @Author: 骆金参
# @Date:   2017-02-26T21:29:23+08:00
# @Email:  1095947440@qq.com
# @Filename: method-rewrite.py
# @Last modified by:   骆金参
# @Last modified time: 2017-04-01T15:35:49+08:00


#!/usr/bin/python3

class Parent:        # 定义父类
   def myMethod(self):
      print ('调用父类方法')

class Child(Parent): # 定义子类
   def myMethod(self):
      print ('调用子类方法')

c = Child()          # 子类实例
c.myMethod()         # 子类调用重写方法

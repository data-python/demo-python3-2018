# @Author: 骆金参
# @Date:   2017-02-26T21:22:39+08:00
# @Email:  1095947440@qq.com
# @Filename: people.py
# @Last modified by:   骆金参
# @Last modified time: 2017-04-01T15:35:53+08:00


#!/usr/bin/python3

#类定义
class people:
    #定义基本属性
    name = ''
    age = 0

    #定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0

    #定义构造方法
    def __init__(self,n,a,w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %d 岁。" %(self.name,self.age))

# 实例化类
p = people('runoob',10,30)
p.speak()

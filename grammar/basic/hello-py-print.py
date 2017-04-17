# @Author: 骆金参 <luo0412>
# @Date:   2017-02-25T12:38:12+08:00
# @Email:  1095947440@qq.com
# @Filename: hello-py-print.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:27:09+08:00


# !/usr/bin/python3

# 输出
print("hello")
# print "python" # 使用python2语法会报错



# 声名
counter = 100
miles = 1000.0  # 浮点型变量
name = "runoob"

print(counter)
print(miles)
print(name)
print(counter, miles, name) # 以空格间隔



# 多个变量赋值
a, b, c = 1, 2, "runoob"
print(a); print(b); print(c);



# 输出类型
a, b, c, d = 20, 5.5, True, 4+3j
print(type(a), type(b), type(c), type(d))
# <class 'int'> <class 'float'> <class 'bool'> <class 'complex'>



# 删除
del a, b
print(a)
# name 'a' is not defined

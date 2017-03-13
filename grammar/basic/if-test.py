# @Author: 骆金参 <luo0412>
# @Date:   2017-02-25T22:07:54+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: if-test.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:11:18+08:00
# @License: MIT



#!/usr/bin/python3

# var1 = 100
# if var1:
#    print ("1 - if 表达式条件为 true")
#    print (var1)
#
# var2 = 0
# if var2:
#    print ("2 - if 表达式条件为 true")
#    print (var2)
# print ("Good bye!")


# # 程序演示了 == 操作符
# # 使用数字
# print(5 == 6)
# # 使用变量
# x = 5
# y = 5
# print(x == y)


num=int(input("输入一个数字："))
if num%2==0:
    if num%3==0:
        print ("你输入的数字可以整除 2 和 3")
    else:
        print ("你输入的数字可以整除 2，但不能整除 3")
else:
    if num%3==0:
        print ("你输入的数字可以整除 3，但不能整除 2")
    else:
        print  ("你输入的数字不能整除 2 和 3")

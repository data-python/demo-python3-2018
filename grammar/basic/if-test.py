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
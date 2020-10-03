# @Author: 骆金参 <luo0412>
# @Date:   2017-02-25T21:24:39+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: operator.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:11:30+08:00
# @License: MIT


# !/usr/bin/python3

# 声名变量
a = 21
b = 10
c = 0

# 简单运算
c = a + b;
print(c)
c = a * b;
print(c)
c = a / b;
print(c)
c = a % b;
print(c)
print("-----------------")

# 修改变量
a = 2
b = 3
c = a ** b;
print(c)
c = a // b;
print(c)
print("-----------------")

# 位运算符演示
a = 60  # 60 = 0011 1100
b = 13  # 13 = 0000 1101
c = 0

c = a & b;
print(c)  # 12 = 0000 1100
c = a | b;
print(c)  # 61 = 0011 1101
c = a ^ b;
print(c)  # 49 = 0011 0001
c = ~a;
print(c)  # -61 = 1100 0011
c = a << 2;
print(c)  # 240 = 1111 0000
c = a >> 2;
print(c)  # 15 = 0000 1111
print("-----------------")

# 逻辑运算符演示
a = 10
b = 20

# a = 0

if (a and b):
    print("变量 a 和 b 都为 true")
else:
    print("变量 a 和 b 有一个不为 true")

if (a or b):
    print("变量 a 和 b 都为 true，或其中一个变量为 true")
else:
    print("变量 a 和 b 都不为 true")

if not (a and b):
    print("变量 a 和 b 都为 false，或其中一个变量为 false")
else:
    print("变量 a 和 b 都为 true")
print("-----------------")

# 身份运算符演示
a = 20
b = 20

# b = 30

if (a is b):
    print("a 和 b 有相同的标识")
else:
    print("a 和 b 没有相同的标识")

if (id(a) == id(b)):
    print("a 和 b 有相同的标识")
else:
    print("a 和 b 没有相同的标识")

if (a is not b):
    print("4 - a 和 b 没有相同的标识")
else:
    print("4 - a 和 b 有相同的标识")
print("-----------------")

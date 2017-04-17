# @Author: 骆金参 <luo0412>
# @Date:   2017-02-25T22:03:40+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: fabonacci.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:23:41+08:00
# @License: MIT



#!/usr/bin/python3

# Fibonacci series: 斐波纳契数列
# 两个元素的总和确定了下一个数
a, b = 0, 1
while b < 1000:
    print(b, end=', ')  # 关键字end可以用于将结果输出到同一行，或者在输出的末尾添加不同的字符
    a, b = b, a+b

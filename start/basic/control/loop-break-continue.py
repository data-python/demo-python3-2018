# @Author: 骆金参 <luo0412>
# @Date:   2017-02-26T13:29:07+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: loop-break-continue.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:11:26+08:00
# @License: MIT



#!/usr/bin/env python


# break语句
for letter in 'Runoob':  # 第一个实例
    if letter == 'b':
        break
    print('当前字母为 :', letter)

# while语句
var = 10
var = var + 1
while var > 1:
    var = var - 1
    if var == 5:
        # break
        continue
    print('var :', var)

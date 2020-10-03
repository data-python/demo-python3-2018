# @Author: 骆金参 <luo0412>
# @Date:   2017-03-13T11:35:59+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: continue-print-error.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:03:20+08:00
# @License: MIT


# while语句
var = 10
while var > 0:
    if var == 5:
        continue
    print('var :', var)
    var = var - 1

# var : 10
# var : 9
# var : 8
# var : 7
# var : 6
# 并未结束，进入死循环
# 没有出口

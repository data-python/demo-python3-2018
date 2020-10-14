# @Author: 骆金参 <luo0412>
# @Date:   2017-03-13T11:42:06+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: prime-num-judge.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:18:56+08:00
# @License: MIT

# 与for对应的else
i = int(input("请输入一个大于2的整数: "))
print("")

for n in range(2, i + 1):
    for x in range(2, n):
        if n % x == 0:
            print(n, '等于', x, '*', n // x)
            break
    else:
        # 循环中没有找到元素
        # 这是一个指数
        print(n, ' 是质数')

#!/usr/bin/python3

# 打开一个文件
f = open("foo.txt", "r")

# str = f.read()

# str = f.readline()

# str = f.readlines()
# print(str)

for line in f:
    print(line, end='')


# 关闭打开的文件
f.close()
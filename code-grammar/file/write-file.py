#!/usr/bin/python3

# 打开一个文件
f = open("foo.txt", "w")


# f.write( "Python 是一个非常好的语言。\n是的，的确非常好!!\n" )

# num = f.write( "Python 是一个非常好的语言。\n是的，的确非常好!!\n" )
# print(num) # 29 返回字符数

# 不是字符串需要先转换
value = ('www.runoob.com', 14)
s = str(value)
f.write(s)

# 关闭打开的文件
f.close()
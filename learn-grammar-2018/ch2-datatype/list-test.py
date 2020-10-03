#!/usr/bin/python3

# 声名
list = ['abcd', 786, 2.23, 'runoob', 70.2]
tinylist = [123, 'runoob']

# 输出
print(list)
print(list[0])  # 第一个元素
print(list[1:3])  # 从第二个开始输出到第三个元素
print(list[2:])  # 输出从第三个元素开始的所有元素
print(tinylist * 2)  # 输出两次列表
print(list + tinylist)  # 连接列表

# 删除列表项
del list[1]
print(list)

list.append("hello");
print(list)
list.insert(2, "bye");
print(list)
print(list.index("hello"))

# 复制
copylist = list[:];
print(copylist)
list[3] = 'w3c'
print(list)
print(copylist);

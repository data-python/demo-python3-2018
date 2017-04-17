#!/usr/bin/python3

# 声名dict
dict = {}
dict['one'] = "1 - 菜鸟教程"
dict[2] = "2 - 菜鸟工具"

tinydict = {'name': 'runoob', 'code': 1, 'site': 'www.runoob.com'}

# 输出
print(dict['one'])
print(dict[2])

# 键值
print(tinydict)
print(tinydict.keys())   # 输出所有键
print(tinydict.values())  # 输出所有值

# 改变字典的方法
tinydict.clear(); print(tinydict)

# @Author: 骆金参
# @Date:   2017-02-26T22:20:21+08:00
# @Email:  1095947440@qq.com
# @Filename: re-sub.py
# @Last modified by:   骆金参
# @Last modified time: 2017-04-01T15:35:16+08:00


#!/usr/bin/python3
import re

phone = "2004-959-559 # 这是一个电话号码"
print (re.sub(r'#.*$', "", phone)) # 删除注释
print (re.sub(r'\D', "", phone)) # 移除非数字的内容


# 将匹配的数字乘于 2
def double(matched):
    value = int(matched.group('value'))
    return str(value * 2)

s = 'A23G4HFD567'
print(re.sub('(?P<value>\d+)', double, s))

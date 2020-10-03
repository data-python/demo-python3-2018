# @Author: 骆金参
# @Date:   2017-02-26T22:16:08+08:00
# @Email:  1095947440@qq.com
# @Filename: re-match-search.py
# @Last modified by:   骆金参
# @Last modified time: 2017-04-01T14:05:27+08:00

# !/usr/bin/python3

import re

str = 'www.www.com'
print(re.match('www', str).span())  # 在起始位置匹配 (0, 3)
print(re.match('con', str))  # NONE

print(re.search('www', str).span())  # 在起始位置匹配
print(re.search('com', str).span())
print(re.search('www', str))
# <_sre.SRE_Match object; span=(0, 3), match='www'>


line = "Cats are smarter than dogs"
matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
searchObj = re.search(r'(.*) are (.*?) .*', line, re.M | re.I)

if matchObj:
    print("matchObj.group() : ", matchObj.group())
    print("matchObj.group(1) : ", matchObj.group(1))
    print("matchObj.group(2) : ", matchObj.group(2))
else:
    print("No match!!")
# matchObj.group() :  Cats are smarter than dogs
# matchObj.group(1) :  Cats
# matchObj.group(2) :  smarter


if searchObj:
    print("searchObj.group() : ", searchObj.group())
    print("searchObj.group(1) : ", searchObj.group(1))
    print("searchObj.group(2) : ", searchObj.group(2))
else:
    print("Nothing found!!")

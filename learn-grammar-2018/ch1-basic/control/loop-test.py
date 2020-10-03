# @Author: 骆金参 <luo0412>
# @Date:   2017-02-25T22:11:48+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: loop-test.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:11:28+08:00
# @License: MIT


# !/usr/bin/python3

sites = ["Baidu", "Google", "Runoob", "Taobao"]
for site in sites:
    if site == "Runoob":
        print("菜鸟教程!")
        break
    print("循环数据 " + site)
else:
    print("没有循环数据!")
print("完成循环!")

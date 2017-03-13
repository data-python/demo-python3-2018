# @Author: 骆金参 <luo0412>
# @Date:   2017-02-25T22:07:11+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: dog-age.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:16:07+08:00

#!/usr/bin/python3

age = int(input("请输入你家狗狗的年龄: "))
print("")  # 换行

if age < 0:
	print("你是在逗我吧!")
elif age == 1:
	print("相当于 14 岁的人。")
elif age == 2:
	print("相当于 22 岁的人。")
elif age > 2:
	human = 22 + (age - 2)*5
	print("对应人类年龄: ", human)

input("点击 enter 键退出")  #退出提示

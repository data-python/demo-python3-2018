# @Author: 骆金参 <luo0412>
# @Date:   2017-02-25T22:09:24+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: guess-num.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:25:10+08:00
# @License: MIT

#!/usr/bin/python3

# 该实例演示了数字猜谜游戏
number = 7
guess = -1 # 全局
print("数字猜谜游戏!")

# 注意终止条件
while guess != number:
    guess = int(input("请输入你猜的数字："))

    if guess == number:
        print("恭喜，你猜对了！")
    elif guess < number:
        print("猜的数字小了...")
    elif guess > number:
        print("猜的数字大了...")

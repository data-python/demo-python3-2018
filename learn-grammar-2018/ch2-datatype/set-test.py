#!/usr/bin/python3
student = ({'Tom', 'Jim', 'Mary', 'Tom', 'Jack', 'Rose'})
print(student)  # 自动去重

# 成员测试
if 'Rose' in student:
    print('Rose 在集合中')
else:
    print('Rose 不在集合中')


# ===
# set可以进行集合运算
a = set('abracadabra')
b = set('alabama')

print(a)
print(a - b)  # a和b的差集
print(a | b)  # a和b的并集
print(a & b)  # a和b的交集
print(a ^ b)  # a和b中不同时存在的元素

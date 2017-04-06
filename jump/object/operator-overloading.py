# @Author: 骆金参
# @Date:   2017-02-26T21:33:07+08:00
# @Email:  1095947440@qq.com
# @Filename: operator-overloading.py
# @Last modified by:   骆金参
# @Last modified time: 2017-04-01T15:35:51+08:00


#!/usr/bin/python3

class Vector:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return 'Vector (%d, %d)' % (self.a, self.b)

    def __add__(self, other):
        return Vector(self.a + other.a, self.b + other.b)


v1 = Vector(2, 10)
v2 = Vector(5, -2)
print(v1 + v2)

# @Author: 骆金参 <luo0412>
# @Date:   2017-02-26T18:54:36+08:00
# @Email:  1095947440@qq.com
# @Project: hello-python
# @Filename: output-test.py
# @Last modified by:   luo0412
# @Last modified time: 2017-03-13T12:11:32+08:00
# @License: MIT



x = 10 * 3.25
y = 200 * 200

hello = 'hello, runoob\n'
hellos = repr(hello)

print(hellos)
# 'hello, runoob\n'

# repr() 的参数可以是 Python 的任何对象
print(repr((x, y, ('Google', 'Runoob'))))
# "(32.5, 40000, ('Google', 'Runoob'))"

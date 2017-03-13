x = 10 * 3.25
y = 200 * 200

hello = 'hello, runoob\n'
hellos = repr(hello)

print(hellos)
# 'hello, runoob\n'

# repr() 的参数可以是 Python 的任何对象
print(repr((x, y, ('Google', 'Runoob'))))
# "(32.5, 40000, ('Google', 'Runoob'))"
f = open('foo.txt', 'rb+')

f.write(b'0123456789abcdef')

print(f.seek(5))     # 移动到文件的第六个字节
# 5

print(f.read(1))
# b'5'

print(f.seek(-3, 2)) # 移动到文件的倒数第三字节
# 13

print(f.read(1))
# b'd'
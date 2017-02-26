import fibo

fibo.fib(1000)
# 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987

print(fibo.fib2(100))
# [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

print(fibo.__name__)
# 'fibo'

# 如果你打算经常使用一个函数
# 你可以把它赋给一个本地的名称：
local_fib = fibo.fib
local_fib(500)
# 1 1 2 3 5 8 13 21 34 55 89 144 233 377


if __name__ == '__main__':
   print('程序自身在运行')
else:
   print('我来自另一模块')

#!/usr/bin/python3

# # 可写函数说明
# def printinfo(name, age):
#     "打印任何传入的字符串"
#     print("名字: ", name);
#     print("年龄: ", age);
#     return;
#
#
# # 调用printinfo函数
# printinfo(age=50, name="runoob");


# # 默认参数
# def printinfo(name, age=35):
#     "打印任何传入的字符串"
#     print("名字: ", name);
#     print("年龄: ", age);
#     return;
#
# # 调用printinfo函数
# printinfo(age=50, name="runoob");
# print("------------------------")
# printinfo(name="runoob");


# 不定长参数
def printinfo(arg1, *vartuple):
    "打印任何传入的参数"
    print("输出: ")
    print(arg1)
    for var in vartuple:
        print(var)
    return;

# 调用printinfo 函数
printinfo(10);
printinfo(70, 60, 50);

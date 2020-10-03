#!/usr/bin/python3

# 模块导入
import numpy as np
from collections import defaultdict
from operator import itemgetter


# 定义变量
dataset_file = "affinity_dataset.txt"
X = np.loadtxt(dataset_file)

valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)
num_occurances = defaultdict(int)

features = ["bread", "milk", "cheese", "apples", "bananas"]
n_features = 5

# # display the first 5 lines
# print(X[:5])


# # 数据样式
# n_samples, n_features = X.shape
# print("This dataset has {0} samples "
#       "and {1} features".format(n_samples, n_features))


# 计算sample中苹果购买次数
# apple_pur_num = 0
#
# for sample in X:
#     if sample[3] == 1:
#         apple_pur_num += 1
# print("苹果num", apple_pur_num) # 36


# 遍历数组存储信息
for sample in X:
    for premise in range(n_features):
        if sample[premise] == 0: continue
        num_occurances[premise] += 1
        for conclusion in range(n_features):
            if premise == conclusion: continue
            if sample[conclusion] == 1:
                valid_rules[(premise, conclusion)] += 1
            else:
                invalid_rules[(premise,conclusion)] += 1

# 输出有效规则
# print(valid_rules)


# 定义输出函数
def print_rule(premise, conclusion, support, confidence, features):
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    print("Rule: If a person buys {0} they will also buy {1}".format(premise_name, conclusion_name))
    print(" - Support: {0}".format(support[(premise,conclusion)]))
    print(" - Confidence: {0:.3f}".format(confidence[(premise,conclusion)]))


# 定义支持度和自信度
support = valid_rules
confidence = defaultdict(float)

# 计算支持度和自信度
for premise, conclusion in valid_rules.keys():
    rule = (premise, conclusion)
    confidence[rule] = valid_rules[rule] / num_occurances[premise]


# # 输出所有的规则及其支持度自信度
# for premise, conclusion in confidence:
#    print_rule(premise, conclusion, support, confidence, features)


# 定义排序的结构
sorted_support = sorted(support.items(), key=itemgetter(1), reverse=True)

# 输出前5的规则
for index in range(5):
    print("Rule #{0}".format(index + 1))
    premise, conclusion = sorted_support[index][0]
    print_rule(premise, conclusion, support, confidence, features)

#!/usr/bin/python3
# @Author: 骆金参
# @Data:   data from http://grouplens.org/datasets/movielens/
# @Date:   2017-03-20T13:00:44+08:00
# @Email:  1095947440@qq.com
# @Last modified by:   骆金参
# @Last modified time: 2017-03-20T15:24:00+08:00

# 导入包===========================================
import os
import sys
import pandas as pd # main
from collections import defaultdict
from operator import itemgetter


# 读取文件=========================================
# 转化时间戳字段格式
all_ratings = pd.read_csv("ml-100k/u.data",
                          delimiter="\t", # 数据是tab分隔
                          header=None,    # 没有表头，自己指定
                          names=["userId","movieId", "rating", "timestamp"])
all_ratings['datetime'] = pd.to_datetime(
                            all_ratings['timestamp'],
                            unit='s') # 时间戳转化为日期格式
# print(all_ratings[:5] , "\n") # 打印前5行


# 增加字段Favorable
# 判断用户是否喜欢该电影========================================
all_ratings["Favorable"] = all_ratings["rating"] > 3 # 判断条件 rating > 3
# print(all_ratings[10:15]) # 判断10-14位用户是否喜欢电影


# 前200位用户的打分数据 ==============================
ratings = all_ratings[all_ratings['userId'].isin(range(200))]
favorable_ratings = ratings[ratings["Favorable"]] # 只包括用户喜欢某部电影的数据行
# print(favorable_ratings[:5]) # 输出前5


# 每个用户各喜欢哪些电影===============================
# 按照User ID进行分组
# 把 v.values 存储为 frozenset
# 便于快速判断用户是否为某部电影打过分
favorable_reviews_by_users = dict(
    (k, frozenset(v.values))
    for k, v
    in favorable_ratings.groupby("userId")["movieId"])
# print(len(favorable_reviews_by_users)) # 199


# 每部电影的影迷数量 ======================================
num_favorable_by_movie = ratings[["movieId", "Favorable"]].groupby("movieId").sum()
# print(num_favorable_by_movie.sort_values(by="Favorable", ascending=False)[:5]) # 输出影迷数前5的电影


# 函数=================================================
# 寻找频繁项
# 本算法核心之一
def find_frequent_itemsets(favorable_reviews_by_users, k_1_itemsets, min_support):
    counts = defaultdict(int)

    for user, reviews in favorable_reviews_by_users.items():
        for itemset in k_1_itemsets:
            if itemset.issubset(reviews): # 如果是，表示用户打过分
                for other_reviewed_movie in reviews - itemset: # 用户打过分但不在频繁项集内
                    current_superset = itemset | frozenset((other_reviewed_movie,)) # 超集
                    counts[current_superset] += 1 # 超集支持度+1

    return dict([(itemset, frequency)
                 for itemset, frequency in counts.items()
                 if frequency >= min_support])


# 寻找频繁项集和预备项集 ======================================================
# k=1 candidates are the isbns with
# more than min_support favourable reviews
frequent_itemsets = {}  # itemsets are sorted by length
min_support = 50 # 好评50次以上的

# 算出 length = 1 的所有频繁项集（support>50）
frequent_itemsets[1] = dict(
    (frozenset((movie_id,)), row["Favorable"])
    for movie_id, row
    in num_favorable_by_movie.iterrows() # 列表迭代器
        if row["Favorable"] > min_support
)

# 输出超过最小支持度的电影
# print("There are {} movies with more than {} favorable reviews".format(
#         len(frequent_itemsets[1]),
#         min_support)) # There are 16 movies with more than 50 favorable reviews
# sys.stdout.flush() # 将缓冲区的内容输出到终端


# 寻找频繁项==============================================
for k in range(2, 20):
    # Generate candidates of length k, using the frequent itemsets of length k-1
    # Only store the frequent itemsets
    cur_frequent_itemsets = find_frequent_itemsets(
                favorable_reviews_by_users,
                frequent_itemsets[k-1], # 注意 k-1
                min_support)

    if len(cur_frequent_itemsets) == 0:
        print("没有找到长度为 {} 的频繁项集, 查找结束!!\n".format(k))
        sys.stdout.flush()
        break
    else:
        print("长度为 {} 的频繁项集 {} 个".format( k, len(cur_frequent_itemsets)))
        # print(cur_frequent_itemsets)
        sys.stdout.flush()
        frequent_itemsets[k] = cur_frequent_itemsets


del frequent_itemsets[1] # We aren't interested in the itemsets of length 1, so remove those

# print("Found a total of {0} frequent itemsets"
#       .format(sum(len(itemsets) for itemsets in frequent_itemsets.values())))


# 创建关联规则 ===================================================
# Now we create the association rules.
# First, they are candidates until the confidence has been tested
candidate_rules = []
for itemset_length, itemset_counts in frequent_itemsets.items():
    for itemset in itemset_counts.keys():
        for conclusion in itemset:
            premise = itemset - set((conclusion,))
            candidate_rules.append((premise, conclusion))
# print("There are {} candidate rules".format(len(candidate_rules)))
# print(candidate_rules[:5]) # 5152


# 计算置信度 ==================================================
# # Now, we compute the confidence of each of these rules.
# This is very similar to what we did in chapter 1
correct_counts = defaultdict(int)
incorrect_counts = defaultdict(int)
for user, reviews in favorable_reviews_by_users.items():
    for candidate_rule in candidate_rules:
        premise, conclusion = candidate_rule
        if premise.issubset(reviews):
            if conclusion in reviews:
                correct_counts[candidate_rule] += 1
            else:
                incorrect_counts[candidate_rule] += 1
rule_confidence = {candidate_rule: correct_counts[candidate_rule] / float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule])
              for candidate_rule in candidate_rules}


min_confidence = 0.9 # Choose only rules above a minimum confidence level

# Filter out the rules with poor confidence
rule_confidence = {rule: confidence for rule, confidence in rule_confidence.items() if confidence > min_confidence}
# print(len(rule_confidence))


sorted_confidence = sorted(rule_confidence.items(),
                           key=itemgetter(1),
                           reverse=True)

# for index in range(5):
#     print("Rule #{0}".format(index + 1))
#     (premise, conclusion) = sorted_confidence[index][0]
#     print("Rule: 如果一个人推荐 {0} \n那么他也会推荐 {1}".format(premise, conclusion))
#     print(" - Confidence: {0:.3f}".format(rule_confidence[(premise, conclusion)]))
#     print("")


# Even better===================================================
# we can get the movie titles themselves from the dataset
movie_name_data = pd.read_csv("ml-100k/u.item",
                              delimiter="|",
                              header=None,
                              encoding = "mac-roman")
movie_name_data.columns = ["movieId", "title", "Release Date",
                        "Video Release", "IMDB", "<UNK>", "Action", "Adventure",
                        "Animation", "Children's", "Comedy", "Crime", "Documentary",
                        "Drama", "Fantasy", "Film-Noir",
                        "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller",
                        "War", "Western"]

def get_movie_name(movie_id):
    title_object = movie_name_data[movie_name_data["movieId"] == movie_id]["title"]
    title = title_object.values[0]
    return title

# print("id=4的电影为: " , get_movie_name(4) , "\n") # 获取id=4的电影


# 输出前5条规则
for index in range(5):
    print("前排推荐{0}==================".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    premise_names = "\n".join(get_movie_name(idx) for idx in premise)
    conclusion_name = get_movie_name(conclusion)
    print("如果一个人推荐了\n{0} \n\n那么他也会推荐\n{1}".format(premise_names, conclusion_name))
    print("(置信度 = {0:.3f})".format(rule_confidence[(premise, conclusion)]))
    print("")


# Evaluation using test data==========================================
# test_dataset = all_ratings[~all_ratings['userId'].isin(range(200))]
# test_favorable = test_dataset[test_dataset["Favorable"]]
# test_not_favourable = test_dataset[~test_dataset["Favorable"]]
# test_favorable_by_users = dict((k, frozenset(v.values)) for k, v in test_favorable.groupby("userId")["movieId"])
# test_not_favourable_by_users = dict((k, frozenset(v.values)) for k, v in test_not_favourable.groupby("userId")["movieId"])
# test_users = test_dataset["userId"].unique()
#
#
# correct_counts = defaultdict(int)
# incorrect_counts = defaultdict(int)
# for user, reviews in test_favorable_by_users.items():
#     for candidate_rule in candidate_rules:
#         premise, conclusion = candidate_rule
#         if premise.issubset(reviews):
#             if conclusion in reviews:
#                 correct_counts[candidate_rule] += 1
#             else:
#                 incorrect_counts[candidate_rule] += 1
#
#
# test_confidence = {candidate_rule: correct_counts[candidate_rule] / float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule])
#                    for candidate_rule in rule_confidence}
# print(len(test_confidence))
#
#
# sorted_test_confidence = sorted(test_confidence.items(), key=itemgetter(1), reverse=True)
# print(sorted_test_confidence[:5])
#
#
# for index in range(10):
#     print("Rule #{0}".format(index + 1))
#     (premise, conclusion) = sorted_confidence[index][0]
#     premise_names = ", ".join(get_movie_name(idx) for idx in premise)
#     conclusion_name = get_movie_name(conclusion)
#     print("Rule: If a person recommends {0} they will also recommend {1}".format(premise_names, conclusion_name))
#     print(" - Train Confidence: {0:.3f}".format(rule_confidence.get((premise, conclusion), -1)))
#     print(" - Test Confidence: {0:.3f}".format(test_confidence.get((premise, conclusion), -1)))
#     print("")

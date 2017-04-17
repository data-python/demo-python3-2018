# @Author: 骆金参
# @Date:   2017-03-18T18:59:25+08:00
# @Email:  1095947440@qq.com
# @Filename: apriori-test.py
# @Last modified by:   骆金参
# @Last modified time: 2017-03-20T12:50:43+08:00


#!/usr/bin/python3

# data from http://grouplens.org/datasets/movielens/

# import os
import pandas as pd
from collections import defaultdict
import sys

# data_folder = os.path.abspath("E:\06-Python\hello-python\lab\lab2\data")
# ratings_filename = os.path.join(data_folder, "rating.csv")

all_ratings = pd.read_csv("data/ratings.csv")
# print(all_ratings[:5]) # 打印前5行

all_ratings["Favorable"] = all_ratings["rating"] > 3
# print(all_ratings[10:15]) # 判断10-14是否喜欢这部电影

ratings = all_ratings[all_ratings['userId'].isin(range(200))]
favorable_ratings = ratings[ratings["Favorable"]]
# print(favorable_ratings[:5]) # 打印评分前5喜欢的电影

# 各个用户各喜欢哪些电影
# 遍历每个用户看过的每一部电影
favorable_reviews_by_users = \
    dict((k, frozenset(v.values)) for k, v
         in favorable_ratings.groupby("userId")["movieId"])
# print(len(favorable_reviews_by_users)) # 199

# 最受欢迎的5部电影
num_favorable_by_movie = ratings[["movieId", "Favorable"]].groupby("movieId").sum()
# print(num_favorable_by_movie.sort_values(by="Favorable", ascending=False)[:5])


# 函数
# 寻找频繁项
def find_frequent_itemsets(favorable_reviews_by_users, k_1_itemsets, min_support):
    counts = defaultdict(int)
    for user, reviews in favorable_reviews_by_users.items():
        for itemset in k_1_itemsets:
            if itemset.issubset(reviews):
                for other_reviewed_movie in reviews - itemset:
                    current_superset = itemset | frozenset((other_reviewed_movie,))
                    counts[current_superset] += 1
    return dict([(itemset, frequency)
                 for itemset, frequency in counts.items()
                 if frequency >= min_support])



frequent_itemsets = {}  # itemsets are sorted by length
min_support = 50

# k=1 candidates are the isbns with more than min_support favourable reviews
frequent_itemsets[1] = dict((frozenset((movie_id,)), row["Favorable"])
                                for movie_id, row in num_favorable_by_movie.iterrows()
                                if row["Favorable"] > min_support)

print("There are {} movies with more than {} favorable reviews".format(len(frequent_itemsets[1]), min_support))
sys.stdout.flush()

# 输出结果
# There are 21 movies with more than 50 favorable reviews


for k in range(2, 20):
    # Generate candidates of length k, using the frequent itemsets of length k-1
    # Only store the frequent itemsets
    cur_frequent_itemsets = find_frequent_itemsets(favorable_reviews_by_users, frequent_itemsets[k-1],
                                                   min_support)
    if len(cur_frequent_itemsets) == 0:
        print("Did not find any frequent itemsets of length {}".format(k))
        sys.stdout.flush()
        break
    else:
        print("I found {} frequent itemsets of length {}".format(len(cur_frequent_itemsets), k))
        #print(cur_frequent_itemsets)
        sys.stdout.flush()
        frequent_itemsets[k] = cur_frequent_itemsets

# We aren't interested in the itemsets of length 1, so remove those
del frequent_itemsets[1]

# 输出结果
# I found 157 frequent itemsets of length 2
# I found 590 frequent itemsets of length 3
# I found 1250 frequent itemsets of length 4
# I found 1596 frequent itemsets of length 5
# I found 1279 frequent itemsets of length 6
# I found 650 frequent itemsets of length 7
# I found 199 frequent itemsets of length 8
# I found 32 frequent itemsets of length 9
# I found 2 frequent itemsets of length 10
# Did not find any frequent itemsets of length 11

print("Found a total of {0} frequent itemsets"
      .format(sum(len(itemsets) for itemsets in frequent_itemsets.values())))


# Now we create the association rules. First, they are candidates until the confidence has been tested
candidate_rules = []
for itemset_length, itemset_counts in frequent_itemsets.items():
    for itemset in itemset_counts.keys():
        for conclusion in itemset:
            premise = itemset - set((conclusion,))
            candidate_rules.append((premise, conclusion))
print("There are {} candidate rules".format(len(candidate_rules)))

print(candidate_rules[:5])


# Now, we compute the confidence of each of these rules. This is very similar to what we did in chapter 1
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


# Choose only rules above a minimum confidence level
min_confidence = 0.9

# Filter out the rules with poor confidence
rule_confidence = {rule: confidence for rule, confidence in rule_confidence.items() if confidence > min_confidence}
print(len(rule_confidence))

from operator import itemgetter
sorted_confidence = sorted(rule_confidence.items(), key=itemgetter(1), reverse=True)


for index in range(5):
    print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    print("Rule: If a person recommends {0} they will also recommend {1}".format(premise, conclusion))
    print(" - Confidence: {0:.3f}".format(rule_confidence[(premise, conclusion)]))
    print("")

# @Author: 骆金参
# @Date:   2017-03-18T20:43:34+08:00
# @Email:  1095947440@qq.com
# @Filename: apriori-better.py
# @Last modified by:   骆金参
# @Last modified time: 2017-03-20T13:00:54+08:00


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

# Even better, we can get the movie titles themselves from the dataset
#  movie_name_filename = os.path.join(data_folder, "u.item")
movie_name_filename = "data/movies.csv"
movie_name_data = pd.read_csv(movie_name_filename)
movie_name_data.columns = ["movieId", "title", "genres"]

def get_movie_name(movie_id):
    title_object = movie_name_data[movie_name_data["movieId"] == movie_id]["title"]
    title = title_object.values[0]
    return title

print(get_movie_name(4))


for index in range(5):
    print("Rule #{0}".format(index + 1))
    (premise, conclusion) = sorted_confidence[index][0]
    premise_names = ", ".join(get_movie_name(idx) for idx in premise)
    conclusion_name = get_movie_name(conclusion)
    print("Rule: If a person recommends {0} they will also recommend {1}".format(premise_names, conclusion_name))
    print(" - Confidence: {0:.3f}".format(rule_confidence[(premise, conclusion)]))
    print("")











# # Evaluation using test data
# test_dataset = all_ratings[~all_ratings['UserID'].isin(range(200))]
# test_favorable = test_dataset[test_dataset["Favorable"]]
# #test_not_favourable = test_dataset[~test_dataset["Favourable"]]
# test_favorable_by_users = dict((k, frozenset(v.values)) for k, v in test_favorable.groupby("UserID")["MovieID"])
# #test_not_favourable_by_users = dict((k, frozenset(v.values)) for k, v in test_not_favourable.groupby("UserID")["MovieID"])
# #test_users = test_dataset["UserID"].unique()
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
#


# Found a total of 5755 frequent itemsets
# There are 29188 candidate rules
# [(frozenset({1196}), 2858), (frozenset({2858}), 1196), (frozenset({2571}), 4993), (frozenset({4993}), 2571), (frozenset({1270}), 1210)]
# 9245
# Rule #1
# Rule: If a person recommends frozenset({2858, 1196, 1198, 593, 1270, 1210}) they will also recommend 260
#  - Confidence: 1.000
#
# Rule #2
# Rule: If a person recommends frozenset({1210, 260, 589, 318, 1198}) they will also recommend 1196
#  - Confidence: 1.000
#
# Rule #3
# Rule: If a person recommends frozenset({4993, 356, 260, 2571, 527, 1270}) they will also recommend 318
#  - Confidence: 1.000
#
# Rule #4
# Rule: If a person recommends frozenset({260, 2571, 356, 589}) they will also recommend 1196
#  - Confidence: 1.000
#
# Rule #5
# Rule: If a person recommends frozenset({260, 296, 2858, 2571, 1198, 2959}) they will also recommend 1196
#  - Confidence: 1.000
#
# Waiting to Exhale (1995)
# Rule #1
# Rule: If a person recommends American Beauty (1999), Star Wars: Episode V - The Empire Strikes Back (1980), Raiders of the Lost Ark (Indiana Jones and the Raiders of the Lost Ark) (1981), Silence of the Lambs, The (1991), Back to the Future (1985), Star Wars: Episode VI - Return of the Jedi (1983) they will also recommend Star Wars: Episode IV - A New Hope (1977)
#  - Confidence: 1.000
#
# Rule #2
# Rule: If a person recommends Star Wars: Episode VI - Return of the Jedi (1983), Star Wars: Episode IV - A New Hope (1977), Terminator 2: Judgment Day (1991), Shawshank Redemption, The (1994), Raiders of the Lost Ark (Indiana Jones and the Raiders of the Lost Ark) (1981) they will also recommend Star Wars: Episode V - The Empire Strikes Back (1980)
#  - Confidence: 1.000
#
# Rule #3
# Rule: If a person recommends Lord of the Rings: The Fellowship of the Ring, The (2001), Forrest Gump (1994), Star Wars: Episode IV - A New Hope (1977), Matrix, The (1999), Schindler's List (1993), Back to the Future (1985) they will also recommend Shawshank Redemption, The (1994)
#  - Confidence: 1.000
#
# Rule #4
# Rule: If a person recommends Star Wars: Episode IV - A New Hope (1977), Matrix, The (1999), Forrest Gump (1994), Terminator 2: Judgment Day (1991) they will also recommend Star Wars: Episode V - The Empire Strikes Back (1980)
#  - Confidence: 1.000
#
# Rule #5
# Rule: If a person recommends Star Wars: Episode IV - A New Hope (1977), Pulp Fiction (1994), American Beauty (1999), Matrix, The (1999), Raiders of the Lost Ark (Indiana Jones and the Raiders of the Lost Ark) (1981), Fight Club (1999) they will also recommend Star Wars: Episode V - The Empire Strikes Back (1980)
#  - Confidence: 1.000
